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
"""Utilities the TeaL websocket dispatcher."""

from __future__ import annotations

from asyncio import gather as gather_asyncio
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncIterator, Literal, TypeVar

from fastapi import WebSocket

from pydantic import BaseModel, Field

from teal.amq import (
    AMQHandler, CallbackMessage, PowensHMACSignature, PowensHookMessage,
)

from .config import Settings

WebsocketDispatcherType = TypeVar(
    'WebsocketDispatcherType',
    bound='WebsocketDispatcher',
)


class CallbackCreation(BaseModel):
    """Data to create a stored callback data."""

    type: Literal['callback']
    """Callback creation type, as a discriminant."""

    state: str
    """The state to create."""

    final_redirect_url: str
    """Final redirect URL."""

    with_fragment: bool = False
    """Whether to get the fragment with the redirect or not."""

    expires_at: datetime
    """Expiration date for the callback creation."""


class CallbackRegistration(BaseModel):
    """Registration for callback states."""

    type: Literal['callback']
    """Callback register type, as a discriminant."""

    state: str
    """The state to register to."""


class PowensDomainRegistration(BaseModel):
    """Registration for events related to a Powens domain."""

    type: Literal['powens_domain']
    """Powens domain register type."""

    powens_domain: str
    """The Powens domain to register, without the '.biapi.pro' domain part."""


class RequestMessage(BaseModel):
    """Message for registering to one or more set of events."""

    create: CallbackCreation | None = Field(default=None)
    """Element to create in the database."""

    register_to: (
        CallbackRegistration
        | PowensDomainRegistration
        | None
    ) = Field(
        default=None,
        discriminator='type',
    )
    """Event to register to."""


class CallbackCreationFailedMessage(BaseModel):
    """Message signalling that registering a callback has failed."""

    type: Literal['callback_creation_failure'] = ('callback_creation_failure')
    """Message type, for allowing discrimination at caller level."""

    state: str
    """State for which the callback event binding has failed."""

    detail: str
    """Human-readable creation failure detail."""


class CallbackPushMessage(BaseModel):
    """Message produced by the server when a callback event occurs."""

    type: Literal['callback'] = ('callback')
    """Message type, for allowing discrimination at caller level."""

    timestamp: datetime
    """Timestamp at which the message was emitted."""

    url: str
    """Resulting callback URL with parameters and fragment."""

    state: str
    """State for which the callback is emitted."""


class PowensHookPushMessage(BaseModel):
    """Message produced by the server when a Powens hook is called."""

    type: Literal['powens_hook'] = ('powens_hook')
    """Message type, for allowing discrimination at caller level."""

    timestamp: datetime
    """Timestamp at which the message was emitted."""

    domain: str
    """Domain for which the webhook is emitted."""

    hook: str
    """Type of hook for which the webhook is emitted."""

    hmac_signature: PowensHMACSignature | None
    """The HMAC signature, if present."""

    user_token: str | None
    """User scoped token with which the hook is authenticated."""

    payload: str
    """The UTF-8 decoded payload."""


class WebsocketDispatcher:
    """Main class for dispatching websocket event pushes."""

    __slots__ = (
        'amq_handler',
        'callback_state_by_websocket',
        'powens_domain_by_websocket',
        'websocket_by_callback_state',
        'websocket_by_powens_domain',
    )

    websocket_by_callback_state: defaultdict[str, set[WebSocket]]
    """Set of websockets bound to a particular callback state."""

    callback_state_by_websocket: defaultdict[WebSocket, set[str]]
    """Set of callback states bound to a particular websocket."""

    websocket_by_powens_domain: defaultdict[str, set[WebSocket]]
    """Set of websockets to which the hooks should be sent for a domain."""

    powens_domain_by_websocket: defaultdict[WebSocket, set[str]]
    """Set of Powens domain whose hooks are sent to a websocket."""

    def __init__(self, /, *, amq_handler: AMQHandler):
        self.amq_handler = amq_handler
        self.websocket_by_callback_state = defaultdict(lambda: set())
        self.callback_state_by_websocket = defaultdict(lambda: set())
        self.websocket_by_powens_domain = defaultdict(lambda: set())
        self.powens_domain_by_websocket = defaultdict(lambda: set())

    @classmethod
    @asynccontextmanager
    async def dispatcher_context(
        cls: type[WebsocketDispatcherType],
        /,
        *,
        settings: Settings,
    ) -> AsyncIterator[WebsocketDispatcherType]:
        """Get a dispatcher in a context.

        :param settings: The settings to use.
        """
        async with AMQHandler.handler_context(
            settings=settings,
        ) as amq_handler:
            dispatcher = cls(amq_handler=amq_handler)
            amq_handler.callback = dispatcher.push
            yield dispatcher

    async def bind_callback_state(
        self, websocket: WebSocket, /, *,
        state: str,
    ) -> None:
        """Bind a websocket to a callback state.

        :param websocket: The websocket to bind.
        :param state: The state to bind to.
        """
        await self.amq_handler.bind_callback_state(state)

        self.websocket_by_callback_state[state].add(websocket)
        self.callback_state_by_websocket[websocket].add(state)

    async def bind_powens_domain(
        self, websocket: WebSocket, /, *,
        domain: str,
    ) -> None:
        """Bind a websocket to Powens hook calls for a domain.

        :param websocket: The websocket to bind.
        :param domain: The domain to bind for, without '.biapi.pro'.
        """
        await self.amq_handler.bind_powens_domain_hooks(domain)

        self.websocket_by_powens_domain[domain].add(websocket)
        self.powens_domain_by_websocket[websocket].add(domain)

    async def unbind_all(self, websocket: WebSocket, /) -> None:
        """Unbind everything from a websocket.

        :param websocket: The websocket to unbind.
        """
        for by_websocket, by_key in (
            (
                self.callback_state_by_websocket,
                self.websocket_by_callback_state,
            ),
            (self.powens_domain_by_websocket, self.websocket_by_powens_domain),
        ):
            keys: set[Any] = by_websocket.pop(websocket, set())
            for key in keys:
                websocket_set = by_key[key]

                try:
                    websocket_set.remove(websocket)
                except KeyError:  # pragma: no cover
                    pass
                else:
                    if not websocket_set:
                        try:
                            del by_key[key]
                        except KeyError:  # pragma: no cover
                            pass

    async def push(
        self,
        message: Any,
        /,
    ) -> None:
        """Push a message.

        :param message: The message to push.
        """
        if isinstance(message, CallbackMessage):
            state = message.state
            push_message = CallbackPushMessage(
                timestamp=message.timestamp,
                state=state,
                url=message.url,
            ).json(separators=(',', ':'))

            gather_asyncio(*(
                websocket.send_text(push_message)
                for websocket in self.websocket_by_callback_state[state]
            ))
        elif isinstance(message, PowensHookMessage):
            domain = message.domain
            push_message = PowensHookPushMessage(
                timestamp=message.timestamp,
                domain=domain,
                hook=message.hook,
                hmac_signature=message.hmac_signature,
                user_token=message.user_token,
                payload=message.payload,
            ).json(separators=(',', ':'))

            gather_asyncio(*(
                websocket.send_text(push_message)
                for websocket in self.websocket_by_powens_domain[domain]
            ))
