#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2023 Thomas Touhey <thomas@touhey.fr>
#
# This software is governed by the CeCILL 2.1 license under French law and
# abiding by the rules of distribution of free software. You can use, modify
# and/or redistribute the software under the terms of the CeCILL 2.1 license as
# circulated by CEA, CNRS and INRIA at the following URL: https://cecill.info
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL 2.1 license and that you accept its terms.
# *****************************************************************************
"""ASGI application for the TeaL web listener."""

from __future__ import annotations

import os
from functools import lru_cache

from fastapi import BackgroundTasks, Depends, FastAPI, Path, Query, Request
from fastapi.responses import PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.status import (
    HTTP_204_NO_CONTENT, HTTP_302_FOUND, HTTP_400_BAD_REQUEST,
)

from teal.amq import AMQHandler, CallbackMessage, Message, PowensHookMessage
from teal.redis import get_stored_state

from .config import Settings
from .utils import (
    PowensHookClientException, QueryStringMiddleware,
    find_state_in_url, get_powens_hmac_signature, get_powens_user_token,
)

__all__ = ['app']

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
"""ASGI application definition for the listener."""

app.add_middleware(QueryStringMiddleware, delimiter='&')

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), 'templates'),
)
static_files = StaticFiles(
    directory=os.path.join(os.path.dirname(__file__), 'static'),
)


async def send_message(
    message: Message,
    /,
    *,
    settings: Settings,
) -> None:  # pragma: no cover
    """Send a message on an AMQ queue.

    :param message: Message to send.
    """
    # NOTE: This is not covered since it is considered tested in
    # ``tests/test_amq.py``.
    async with AMQHandler.handler_context(settings=settings) as handler:
        await handler.send(message)


@lru_cache()
def get_settings() -> Settings:
    """Get settings instanciated per request."""
    return Settings()


@app.get('/favicon.png')
@app.get('/favicon.ico')
@app.get('/robots.txt')
async def get_static_file(request: Request) -> Response:
    """Get static files."""
    _, _, filename = request.url.path.rpartition('/')
    return await static_files.get_response(filename, request.scope)


# ---
# Callback management.
# ---


@app.get('/callback')
@app.get('/errback')
async def get_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    state: str | None = Query(default=None, example='123'),  # noqa: B008
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get a callback event from an end user."""
    if state is None:
        # We suppose that the state is located in the fragment, so we need
        # to redirect to the raw callback endpoint with the full URL including
        # the fragment.
        return templates.TemplateResponse(
            'fragment.html',
            {'request': request},
        )

    if state == '':
        return PlainTextResponse(
            'Empty state\n',
            status_code=HTTP_400_BAD_REQUEST,
        )

    stored_state = await get_stored_state(state, settings=settings)
    if stored_state is None:
        # The state is present but unknown, so we just return an empty
        # HTTP 400 response.
        return PlainTextResponse(
            'Unknown state\n',
            status_code=HTTP_400_BAD_REQUEST,
        )

    if stored_state.with_fragment:
        # We need to get the fragment, even though we have the state.
        return templates.TemplateResponse(
            'fragment.html',
            {'request': request},
        )

    background_tasks.add_task(
        send_message,
        CallbackMessage(
            url=str(request.url),
            state=state,
        ),
        settings=settings,
    )

    if stored_state.final_redirect_url is None:
        return Response(b'', status_code=HTTP_204_NO_CONTENT)

    return RedirectResponse(
        stored_state.final_redirect_url,
        status_code=HTTP_302_FOUND,
    )


@app.get('/raw-callback')
async def get_raw_callback(
    background_tasks: BackgroundTasks,
    full_url: str | None = Query(
        default=None,
        example='https://events.teapots.fr/callback#state=123',
    ),  # noqa: B008
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get a raw callback event from an end user."""
    if full_url is None:
        # We suppose that the state is located in the fragment, so we need
        # to redirect to the raw callback endpoint with the full URL including
        # the fragment.
        return PlainTextResponse(
            'Missing full URL\n',
            status_code=HTTP_400_BAD_REQUEST,
        )

    state = find_state_in_url(full_url)
    if state is None:
        # We suppose that the state is located in the fragment, so we need
        # to redirect to the raw callback endpoint with the full URL including
        # the fragment.
        return PlainTextResponse(
            'Missing state in full URL\n',
            status_code=HTTP_400_BAD_REQUEST,
        )

    if state == '':
        return PlainTextResponse(
            'Empty state\n',
            status_code=HTTP_400_BAD_REQUEST,
        )

    stored_state = await get_stored_state(state, settings=settings)
    if stored_state is None:
        # The state is present but unknown, so we just return an empty
        # HTTP 400 response.
        return PlainTextResponse(
            'Unknown state\n',
            status_code=HTTP_400_BAD_REQUEST,
        )

    background_tasks.add_task(
        send_message,
        CallbackMessage(
            url=full_url,
            state=state,
        ),
        settings=settings,
    )

    if stored_state.final_redirect_url is None:
        return Response(b'', status_code=HTTP_204_NO_CONTENT)

    return RedirectResponse(
        stored_state.final_redirect_url,
        status_code=HTTP_302_FOUND,
    )


# ---
# Powens webhooks management.
# ---


@app.exception_handler(PowensHookClientException)
async def handle_powens_hook_exception(
    request: Request,
    exc: PowensHookClientException,
) -> Response:
    """Handle Powens validation exception.

    Since Powens allows returning the direct responses from our server by mail
    and through logs, we want to return simply the error message.
    """
    return PlainTextResponse(
        content=exc.detail + '\n',
        status_code=exc.status_code,
    )


@app.post('/powens-hook/{domain}/{hook}')
async def get_powens_hook(
    request: Request,
    background_tasks: BackgroundTasks,
    domain: str = Path(
        example='budgea.biapi.pro',
    ),  # noqa: B008
    hook: str = Path(
        example='USER_CREATED',
    ),  # noqa: B008
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get a Powens webhook push."""
    if not domain.endswith('.biapi.pro') or len(domain) <= 10:
        raise PowensHookClientException(detail=(
            'Webhook misconfiguration: endpoint must contain the ".biapi.pro" '
            + 'suffix, such as: '
            + str(request.url_for(
                'get_powens_hook',
                domain=domain + '.biapi.pro',
                hook=hook,
            ))
        ))

    hmac_signature = get_powens_hmac_signature(request)
    user_token = get_powens_user_token(request)

    if hmac_signature is None and user_token is None:
        raise PowensHookClientException(detail=(
            'Webhook misconfiguration: user-scoped token or HMAC '
            + 'authentication required.'
        ))

    payload: bytes = await request.body()

    background_tasks.add_task(
        send_message,
        PowensHookMessage(
            domain=domain,
            hook=hook,
            hmac_signature=hmac_signature,
            user_token=user_token,
            payload=payload.decode('UTF-8'),
        ),
        settings=settings,
    )

    return Response(b'', status_code=HTTP_204_NO_CONTENT)
