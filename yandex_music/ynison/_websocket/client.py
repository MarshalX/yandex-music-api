"""Данный websocket клиент взят из репозитория MarshalX/atproto и адаптирован под Ynison.

Оригинальный код: https://github.com/MarshalX/atproto/blob/8e6fe72d0ce2a0eb7a276cebed180d559fe9aa93/packages/atproto_firehose/client.py
Код лицензирован под MIT license.
"""

import asyncio
import random
import socket
import threading
import time
import traceback
import typing as t
from urllib.parse import urlencode

from websockets.client import connect as aconnect
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    InvalidHandshake,
    PayloadTooBig,
    ProtocolError,
)
from websockets.sync.client import connect

from yandex_music.exceptions import YnisonError

OnConnectCallback = t.Callable[[], None]
AsyncOnConnectCallback = t.Callable[[], t.Coroutine[t.Any, t.Any, None]]

OnMessageCallback = t.Callable[[str], None]
AsyncOnMessageCallback = t.Callable[[str], t.Coroutine[t.Any, t.Any, None]]

OnCallbackErrorCallback = t.Callable[[BaseException], None]
AsyncOnCallbackErrorCallback = t.Callable[[BaseException], t.Coroutine[t.Any, t.Any, None]]

_OK_ERRORS = (ConnectionClosedOK,)
_ERR_ERRORS = (
    ConnectionError,
    ConnectionClosedError,
    InvalidHandshake,
    PayloadTooBig,
    ProtocolError,
    socket.gaierror,
)


if t.TYPE_CHECKING:
    from websockets.client import ClientConnection as SyncWebSocketClient
    from websockets.legacy.client import Connect as AsyncConnect


def _build_websocket_uri(method: str, base_uri: str, params: t.Optional[t.Dict[str, t.Any]] = None) -> str:
    query_string = ''
    if params:
        query_string = f'?{urlencode(params)}'

    return f'{base_uri}/{method}{query_string}'


def _handle_websocket_error_or_stop(exception: Exception) -> bool:
    """Return if the connection should be properly being closed or reraise exception."""
    if isinstance(exception, _OK_ERRORS):
        return True
    if isinstance(exception, _ERR_ERRORS):
        return False

    if isinstance(exception, YnisonError):
        raise exception

    raise YnisonError from exception


class _WebsocketClientBase:
    def __init__(
        self,
        method: str,
        base_uri: str,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        headers: t.Optional[t.Mapping[str, str]] = None,
        subprotocols: t.Optional[t.List[str]] = None,
    ) -> None:
        self._method = method
        self._base_uri = base_uri
        self._params = params
        self._headers = headers
        self._subprotocols = subprotocols

        self._reconnect_no = 0
        self._max_reconnect_delay_sec = 64

        self._client: t.Optional['SyncWebSocketClient'] = None
        self._async_client: t.Optional['AsyncConnect'] = None

    @property
    def _websocket_uri(self) -> str:
        # the user should care about updated params by himself
        return _build_websocket_uri(self._method, self._base_uri, self._params)

    def _get_client(self) -> 'SyncWebSocketClient':
        self._client = connect(
            uri=self._websocket_uri,
            additional_headers=self._headers,
            subprotocols=self._subprotocols,
            close_timeout=0.1,
        )
        return self._client

    def _get_async_client(self) -> 'AsyncConnect':
        self._async_client = aconnect(
            uri=self._websocket_uri,
            extra_headers=self._headers,
            subprotocols=self._subprotocols,
            close_timeout=0.1,
        )
        return self._async_client

    def _get_reconnection_delay(self) -> int:
        base_sec = 2**self._reconnect_no
        rand_sec = random.uniform(-0.5, 0.5)  # noqa: S311

        return min(base_sec, self._max_reconnect_delay_sec) + rand_sec


class _WebsocketClient(_WebsocketClientBase):
    def __init__(
        self,
        method: str,
        base_uri: str,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        headers: t.Optional[t.Mapping[str, str]] = None,
        subprotocols: t.Optional[t.List[str]] = None,
    ) -> None:
        super().__init__(method, base_uri, params, headers, subprotocols)

        self._stop_lock = threading.Lock()

        self._on_message_callback: t.Optional[OnMessageCallback] = None
        self._on_callback_error_callback: t.Optional[OnCallbackErrorCallback] = None

    def _process_message_frame(self, frame: str) -> None:
        try:
            if self._on_message_callback is not None:
                self._on_message_callback(frame)
        except Exception as e:  # noqa: BLE001
            if self._on_callback_error_callback:
                try:
                    self._on_callback_error_callback(e)
                except:  # noqa
                    traceback.print_exc()
            else:
                traceback.print_exc()

    def start(
        self,
        on_message_callback: OnMessageCallback,
        on_callback_error_callback: t.Optional[OnCallbackErrorCallback] = None,
        on_connect_callback: t.Optional[OnConnectCallback] = None,
    ) -> None:
        """Subscribe to Ynison and start client.

        Args:
            on_message_callback: Callback that will be called on the new Ynison message.
            on_callback_error_callback: Callback that will be called if the `on_message_callback` raised an exception.
            on_connect_callback: Callback that will be called on the successful connection.

        Returns:
            :obj:`None`
        """
        self._on_message_callback = on_message_callback
        self._on_callback_error_callback = on_callback_error_callback

        while not self._stop_lock.locked():
            try:
                if self._reconnect_no != 0:
                    time.sleep(self._get_reconnection_delay())

                with self._get_client() as client:
                    self._reconnect_no = 0
                    on_connect_callback and on_connect_callback()

                    while not self._stop_lock.locked():
                        raw_frame = client.recv()
                        if not isinstance(raw_frame, str):
                            # skip non-text frames (should not be occurred)
                            continue

                        self._process_message_frame(raw_frame)

                    self._client = None
            except Exception as e:  # noqa: BLE001
                self._reconnect_no += 1

                should_stop = _handle_websocket_error_or_stop(e)
                if should_stop:
                    break

        if self._stop_lock.locked():
            self._stop_lock.release()

    def send(self, message: str) -> None:
        """Send a message to the Ynison.

        Args:
            message: Message to send.

        Returns:
            :obj:`None`
        """
        if self._client is None:
            raise YnisonError('Клиент не запущен')

        self._client.send(message)

    def send_ping(self) -> None:
        if self._client is None:
            raise YnisonError('Клиент не запущен')

        self._client.ping()

    def stop(self) -> None:
        """Unsubscribe and stop the Ynison client.

        Returns:
            :obj:`None`
        """
        if not self._stop_lock.locked():
            self._stop_lock.acquire()


class _AsyncWebsocketClient(_WebsocketClientBase):
    def __init__(
        self,
        method: str,
        base_uri: str,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        headers: t.Optional[t.Mapping[str, str]] = None,
        subprotocols: t.Optional[t.List[str]] = None,
    ) -> None:
        super().__init__(method, base_uri, params, headers, subprotocols)

        self._stop_event = asyncio.Event()
        self._async_protocol: t.Any = None

        self._on_message_callback: t.Optional[AsyncOnMessageCallback] = None
        self._on_callback_error_callback: t.Optional[AsyncOnCallbackErrorCallback] = None

    async def _process_message_frame(self, frame: str) -> None:
        try:
            if self._on_message_callback is not None:
                await self._on_message_callback(frame)
        except Exception as e:  # noqa: BLE001
            if self._on_callback_error_callback:
                try:
                    await self._on_callback_error_callback(e)
                except:  # noqa
                    traceback.print_exc()
            else:
                traceback.print_exc()

    async def start(
        self,
        on_message_callback: AsyncOnMessageCallback,
        on_callback_error_callback: t.Optional[AsyncOnCallbackErrorCallback] = None,
        on_connect_callback: t.Optional[AsyncOnConnectCallback] = None,
    ) -> None:
        """Subscribe to Ynison and start client.

        Args:
            on_message_callback: Callback that will be called on the new Ynison message.
            on_callback_error_callback: Callback that will be called if the `on_message_callback` raised an exception.
            on_connect_callback: Callback that will be called on the successful connection.

        Returns:
            :obj:`None`
        """
        self._on_message_callback = on_message_callback
        self._on_callback_error_callback = on_callback_error_callback

        while not self._stop_event.is_set():
            try:
                if self._reconnect_no != 0:
                    await asyncio.sleep(self._get_reconnection_delay())

                async with self._get_async_client() as client:
                    self._async_protocol = client
                    self._reconnect_no = 0
                    on_connect_callback and await on_connect_callback()

                    while not self._stop_event.is_set():
                        raw_frame = await client.recv()
                        if not isinstance(raw_frame, str):
                            # skip non-text frames (should not be occurred)
                            continue

                        await self._process_message_frame(raw_frame)

                    self._async_client = None
                    self._async_protocol = None
            except Exception as e:  # noqa: BLE001
                self._reconnect_no += 1

                should_stop = _handle_websocket_error_or_stop(e)
                if should_stop:
                    break

    async def send(self, message: str) -> None:
        """Send a message to the Ynison.

        Args:
            message: Message to send.

        Returns:
            :obj:`None`
        """
        if self._async_protocol is None:
            raise YnisonError('Клиент не запущен')

        await self._async_protocol.send(message)

    async def stop(self) -> None:
        """Unsubscribe and stop the Ynison client.

        Returns:
            :obj:`None`
        """
        self._stop_event.set()


WebsocketClient = _WebsocketClient
AsyncWebsocketClient = _AsyncWebsocketClient
