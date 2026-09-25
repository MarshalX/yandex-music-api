"""Тонкая обёртка над websockets для Ynison.

Используются современные реализации `websockets.sync` и `websockets.asyncio`
(websockets >= 13). Логика переподключения живёт в клиентах, а не здесь.
"""

import inspect
import threading
import time
from typing import Dict, List, Optional

from websockets.asyncio.client import ClientConnection as AsyncConnection
from websockets.asyncio.client import connect as _async_connect
from websockets.exceptions import ConnectionClosed, InvalidStatus, WebSocketException
from websockets.protocol import State
from websockets.sync.client import ClientConnection as SyncConnection
from websockets.sync.client import connect as _sync_connect

__all__ = [
    'AsyncConnection',
    'ConnectionClosed',
    'SyncConnection',
    'WebSocketException',
    'is_auth_failure',
    'open_async',
    'open_sync',
    'start_sync_keepalive',
]

_OPEN_TIMEOUT = 10.0
_CLOSE_TIMEOUT = 0.1
# Состояние с длинной очередью легко превышает дефолтный 1 МиБ websockets.
_MAX_FRAME_SIZE = 64 * 1024 * 1024

# Встроенный keepalive у sync-клиента появился в websockets 15.0.
SYNC_KEEPALIVE_SUPPORTED = 'ping_interval' in inspect.signature(_sync_connect).parameters


def is_auth_failure(exc: BaseException) -> bool:
    """Проверяет, что handshake отклонён из-за аутентификации (HTTP 401/403)."""
    return isinstance(exc, InvalidStatus) and exc.response.status_code in (401, 403)


def open_sync(
    uri: str,
    headers: Dict[str, str],
    subprotocols: List[str],
    ping_interval: Optional[float] = None,
    ping_timeout: Optional[float] = None,
) -> SyncConnection:
    """Открывает синхронное websocket-соединение."""
    kwargs = {}
    if SYNC_KEEPALIVE_SUPPORTED:
        kwargs = {'ping_interval': ping_interval, 'ping_timeout': ping_timeout}

    manager = _sync_connect(
        uri,
        additional_headers=headers,
        subprotocols=subprotocols,
        open_timeout=_OPEN_TIMEOUT,
        close_timeout=_CLOSE_TIMEOUT,
        max_size=_MAX_FRAME_SIZE,
        **kwargs,
    )
    # websockets >= 17.1 без контекстного менеджера выдаёт DeprecationWarning.
    # Закрытие остаётся за клиентом через close().
    return manager.__enter__()


async def open_async(
    uri: str,
    headers: Dict[str, str],
    subprotocols: List[str],
    ping_interval: Optional[float] = None,
    ping_timeout: Optional[float] = None,
) -> AsyncConnection:
    """Открывает асинхронное websocket-соединение."""
    return await _async_connect(
        uri,
        additional_headers=headers,
        subprotocols=subprotocols,
        open_timeout=_OPEN_TIMEOUT,
        close_timeout=_CLOSE_TIMEOUT,
        max_size=_MAX_FRAME_SIZE,
        ping_interval=ping_interval,
        ping_timeout=ping_timeout,
    )


def start_sync_keepalive(connection: SyncConnection, interval: float, timeout: float) -> None:
    """Запускает ping-поток для sync-соединения, если websockets не умеет это сам (< 15.0).

    Поток завершается вместе с соединением. Если pong не пришёл за `timeout`,
    соединение закрывается, и receive-loop клиента уйдёт на переподключение.
    """
    if SYNC_KEEPALIVE_SUPPORTED or not interval:
        return

    def worker() -> None:
        while connection.protocol.state is not State.CLOSED:
            try:
                pong = connection.ping()
            except (ConnectionClosed, RuntimeError):
                return
            if not pong.wait(timeout):
                connection.close()
                return
            time.sleep(interval)

    threading.Thread(target=worker, name='ynison-keepalive', daemon=True).start()
