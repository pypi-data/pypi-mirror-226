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
"""Message queue related utilities for TeaL."""

from __future__ import annotations

from asyncio import Lock as AsyncLock
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from inspect import isawaitable
from logging import getLogger
from typing import Any, AsyncContextManager, AsyncIterator, Callable, TypeVar

from aio_pika import (
    ExchangeType,
    Message as PikaMessage,
    connect_robust as connect_robust_mq,
)
from aio_pika.abc import (
    AbstractChannel, AbstractExchange, AbstractIncomingMessage, AbstractQueue,
)

from pydantic import AmqpDsn, BaseModel, BaseSettings, Field

__all__ = [
    'AMQExchangeName',
    'AMQHandler',
    'AMQSettings',
    'CallbackMessage',
    'Message',
    'PowensHookMessage',
    'PowensHMACSignature',
]

AMQHandlerType = TypeVar('AMQHandlerType', bound='AMQHandler')

logger = getLogger(__name__)

# ---
# Constants and message formats.
# ---


class Message(BaseModel):
    """Base message."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    """UTC date and time at which the message has been sent."""


class CallbackMessage(Message):
    """Body for a callback message in the message queue."""

    url: str
    """Resulting callback URL with parameters and fragment."""

    state: str
    """State for which the callback is emitted."""


class PowensHMACSignature(BaseModel):
    """HMAC signature date for Powens hook body.

    The signature is computed by using the following data::

        BASE_64(
            HMAC_SHA256(
                <METHOD> + "." + <ENDPOINT> + "." + <DATE> + "." + <PAYLOAD>,
                SECRET_KEY
            )
        )

    Where:

    * METHOD is the HTTP method in uppercase.
    * ENDPOINT is the HTTP request path, e.g. "/my-webhook-listener"
    * DATE is the raw "BI-Signature-Date" header.
    * PAYLOAD is the raw webhook data payload.
    """

    signature: str
    """The computed signature on Powens' end."""

    payload_prefix: str
    """The computed prefix to prepend the payload with for computing."""

    signature_date: datetime | None
    """The date and time at which the signature has been produced at."""


class PowensHookMessage(Message):
    """Body for a Powens webhook message in the message queue."""

    domain: str
    """Fully qualified domain for which the webhook is emitted."""

    hook: str
    """Type of hook for which the webhook is emitted."""

    hmac_signature: PowensHMACSignature | None
    """The HMAC signature, if present."""

    user_token: str | None
    """User scoped token with which the hook is authenticated."""

    payload: str
    """The UTF-8 decoded payload."""


# ---
# AMQP related utilities.
# ---


class AMQSettings(BaseSettings):
    """RabbitMQ related settings."""

    amqp_dsn: AmqpDsn = Field(env='AMQP_URL')
    """AMQP connection URI to use.

    An example AMQP URI for localhost is the following:

        amqp://rabbitmq:5672/

    See the `RabbitMQ URI Specification`_ for more information.

    .. _RabbitMQ URI Specification: https://www.rabbitmq.com/uri-spec.html
    """

    amq_exchange_prefix: str = Field(
        default='',
        env='AMQP_EXCHANGE_PREFIX',
    )
    """AMQP exchange name prefix.

    This is mostly useful for cases where TeaL share the same AMQP server for
    multiple applications.
    """


class AMQExchangeName(str, Enum):
    """Exchange names for TeaL AMQ messages."""

    CALLBACKS = ('callbacks')
    """Callback messages.

    :py:class:`CallbackMessage` objects are sent on this exchange, and
    bound by callback state.
    """

    POWENS_DOMAIN_HOOKS = ('powens_domain_hooks')
    """Powens domain hook messages.

    :py:class:`PowensHookMessage` objects are sent on this exchange, and
    bound by Powens domain.
    """


class AMQHandler:
    """AMQ Handler for dispatchers and listeners."""

    __slots__ = (
        'callback',
        '_channel',
        '_connection',
        '_exchange_prefix',
        '_exchanges',
        '_queue',
        '_queue_lock',
    )

    callback: Callable[[Message], Any] | None
    """The callback to call with a message."""

    _exchanges: dict[str, AbstractExchange]
    """The exchanges which we have declared."""

    _queue: AbstractQueue | None
    """The queue used to receive messages."""

    _queue_lock: AsyncLock
    """The lock on the queue property."""

    def __init__(
        self,
        *,
        connection: AsyncContextManager,
        channel: AbstractChannel,
        exchange_prefix: str,
    ) -> None:
        self._channel = channel
        self._connection = connection
        self._exchange_prefix = exchange_prefix
        self._exchanges = {}
        self._queue = None
        self._queue_lock = AsyncLock()

        self.callback = None

    @classmethod
    @asynccontextmanager
    async def handler_context(
        cls: type[AMQHandlerType],
        /,
        *,
        settings: AMQSettings,
    ) -> AsyncIterator[AMQHandlerType]:
        """Get a handler in a context.

        :param settings: The settings to base ourselves on.
        """
        connection = await connect_robust_mq(settings.amqp_dsn)
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=0)

            handler = cls(
                connection=connection,
                channel=channel,
                exchange_prefix=settings.amq_exchange_prefix,
            )
            yield handler

            await handler._channel.close()

    async def get_queue(self, /) -> AbstractQueue:
        """Get the queue for receiving messages."""
        async with self._queue_lock:
            if self._queue is None:
                self._queue = await self._channel.declare_queue()
                await self._queue.consume(self.process)

            return self._queue

    async def get_exchange(
        self,
        name: str,
        /,
        *,
        type_: ExchangeType,
    ) -> AbstractExchange:
        """Get the exchange, declare if necessary.

        :param name: The name of the exchange.
        :param exchange_type: The exchange type.
        :return: The exchange.
        """
        try:
            return self._exchanges[name]
        except KeyError:
            exchange = self._exchanges[name] = (
                await self._channel.declare_exchange(
                    self._exchange_prefix + name,
                    type_,
                )
            )
            return exchange

    async def send(self, message: Message, /) -> None:
        """Send a message on the given context.

        :param message: The message to send.
        """
        if isinstance(message, CallbackMessage):
            exchange_name = AMQExchangeName.CALLBACKS
            routing_key = message.state
        elif isinstance(message, PowensHookMessage):
            exchange_name = AMQExchangeName.POWENS_DOMAIN_HOOKS
            routing_key = message.domain
        else:  # pragma: no cover
            raise TypeError(f'Unsupported message type for {message!r}.')

        exchange = await self.get_exchange(
            exchange_name,
            type_=ExchangeType.DIRECT,
        )
        body = message.json(separators=(',', ':')).encode('utf-8')
        logger.info(
            'Sending message to routing key %r on exchange %r with body %r',
            routing_key,
            body,
        )

        await exchange.publish(
            PikaMessage(body=body),
            routing_key=routing_key,
        )

    async def bind_callback_state(self, state: str, /) -> None:
        """Bind a callback state.

        :param state: The state to bind.
        """
        if not state:
            raise ValueError('State must not be empty to be bound.')

        queue = await self.get_queue()
        exchange = await self.get_exchange(
            AMQExchangeName.CALLBACKS,
            type_=ExchangeType.DIRECT,
        )

        await queue.bind(exchange, state)

    async def bind_powens_domain_hooks(self, domain: str, /) -> None:
        """Bind Powens hooks for a given Powens domain.

        :param domain: The domain to get events for.
        """
        if not domain:
            raise ValueError('Domain must not be empty to be bound.')

        queue = await self.get_queue()
        exchange = await self.get_exchange(
            AMQExchangeName.POWENS_DOMAIN_HOOKS,
            type_=ExchangeType.DIRECT,
        )

        await queue.bind(exchange, domain)

    async def process(
        self,
        incoming_message: AbstractIncomingMessage,
        /,
    ) -> None:
        """Process an incoming message.

        :param message: The incoming message to process.
        """
        callback_func = self.callback
        if callback_func is None:
            return

        exchange_name = incoming_message.exchange
        if exchange_name.startswith(self._exchange_prefix):
            exchange_name = exchange_name[len(self._exchange_prefix):]
        else:
            return

        message: Message
        if exchange_name == AMQExchangeName.CALLBACKS:
            message = CallbackMessage.parse_raw(incoming_message.body)
        elif exchange_name == AMQExchangeName.POWENS_DOMAIN_HOOKS:
            message = PowensHookMessage.parse_raw(incoming_message.body)
        else:
            return

        result = callback_func(message)
        if isawaitable(result):
            await result
