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
"""Utilities for the TeaL web listener."""

from __future__ import annotations

from base64 import b64decode
from datetime import datetime
from urllib.parse import parse_qsl, urlparse

from fastapi import FastAPI, HTTPException, Request

from starlette.status import HTTP_400_BAD_REQUEST
from starlette.types import Receive, Scope, Send

from teal.amq import PowensHMACSignature


class QueryStringMiddleware:
    """Middleware for supporting URLs with a different query string marker.

    This is useful for APIs with weird query string management, such as
    ``https://example.org/callback&state=abc&code=def``, where the query string
    is actually marked with a first ampersand rather than a question mark.
    """

    __slots__ = ('app', 'delimiter')

    app: FastAPI
    """The application on which the middleware should act."""

    delimiter: str
    """The delimiter used as an alternative to ``?``.

    For example, if using ``&`` as the delimiter here, the query string
    determined from the ``https://example.org/callback&state=abc&code=def``
    will be ``state=abc&code=def``.
    """

    def __init__(self, app: FastAPI, *, delimiter: str):
        self.app = app
        self.delimiter = delimiter

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """Process a request with the query string middleware."""
        if scope['type'] == 'http':
            path = scope['path']
            qs = scope['query_string']
            if not qs and self.delimiter in path:
                path, _, qs = path.partition(self.delimiter)
                scope['path'] = path
                scope['query_string'] = qs.encode('utf-8')

        await self.app(scope, receive, send)


class PowensHookClientException(HTTPException):
    """A Powens hook validation has failed.

    :param status_code: The status code to use to signal the error.
        If None, the exception will be reported using the HTTP 400 status
        code.
    """

    def __init__(self, *, status_code: int | None = None, **kwargs):
        if status_code is None:
            status_code = HTTP_400_BAD_REQUEST

        super().__init__(status_code, **kwargs)


def find_state_in_url(url: str, /) -> str | None:
    """Find the state in a given URL.

    Note that this will look for query parameters first, then fragment
    if necessary.

    :param url: The URL to look for a state in.
    :return: The found state, or None if no state could be found.
    """
    parsed_url = urlparse(url)

    # The state might be in the full URL query parameters.
    params = dict(parse_qsl(parsed_url.query, keep_blank_values=True))
    if 'state' in params:
        return params['state']

    # We suppose the fragment is formatted like HTTP parameters, so we
    # want to use this hypothesis to try and get a 'state' in the
    # fragment.
    params = dict(parse_qsl(
        parsed_url.fragment,
        keep_blank_values=True,
    ))
    return params.get('state')


def get_powens_user_token(request: Request) -> str | None:
    """Get the Powens user-scoped token if available.

    For more information, see `Authentication with user-scoped token`_.

    :param request: The request from which to gather a user-scoped token.
    :return: The user-scoped token, or None if no such token could be found.

    .. _`Authentication with user-scoped token`:
        https://docs.powens.com/documentation/integration-guides/webhooks
        #authentication-with-user-scoped-token
    """
    try:
        authorization = request.headers['Authorization']
    except KeyError:
        return None

    auth_type, _, auth_data = authorization.partition(' ')
    if auth_type.casefold() != 'bearer':
        raise PowensHookClientException(
            detail=f'Unhandled authorization type {auth_type!r}',
        )

    if not auth_data:
        raise PowensHookClientException(detail='Missing user-scoped token')

    return auth_data


def get_powens_hmac_signature(request: Request) -> PowensHMACSignature | None:
    """Get the Powens HMAC signature from a fastapi request.

    For more information on the expected headers or header format, see
    `Authentication with a HMAC signature header`_.

    :param request: The request from which to gather the HMAC signature data.
    :return: The HMAC signature, or None if no such signature could be found.

    .. _`Authentication with a HMAC signature header`:
        https://docs.powens.com/documentation/integration-guides/webhooks
        #authentication-with-a-hmac-signature-header
    """
    try:
        signature = request.headers['BI-Signature']
    except KeyError:
        return None

    try:
        raw_signature_date = request.headers['BI-Signature-Date']
    except KeyError:
        raise PowensHookClientException(detail='Missing signature date')

    try:
        # Check that the signature is indeed correctly base64 encoded.
        b64decode(signature, validate=True)
    except ValueError:
        raise PowensHookClientException(detail='Signature is not valid base64')

    try:
        adapted_raw_signature_date = raw_signature_date
        if adapted_raw_signature_date.endswith('Z'):
            adapted_raw_signature_date = (
                adapted_raw_signature_date[:-1] + '+00:00'
            )

        signature_date = datetime.fromisoformat(adapted_raw_signature_date)
    except ValueError:
        raise PowensHookClientException(
            detail='Signature date is not ISO formatted',
        )

    if signature_date.tzinfo is None:
        raise PowensHookClientException(
            detail='Signature date is missing a timezone',
        )

    # Signature prefix is the following:
    # <METHOD> + "." + <ENDPOINT> + "." + <DATE> + "." + <PAYLOAD>
    payload_prefix = (
        f'{request.method.upper()}.{request.url.path}.{raw_signature_date}.'
    )

    return PowensHMACSignature(
        signature=signature,
        payload_prefix=payload_prefix,
        signature_date=signature_date,
    )
