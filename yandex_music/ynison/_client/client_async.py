"""Асинхронный клиент Ynison."""

import asyncio
import contextlib
import inspect
from typing import AsyncIterator, Optional

from yandex_music.exceptions import YnisonError
from yandex_music.ynison import messages
from yandex_music.ynison._client.base import _YnisonClientBase
from yandex_music.ynison._websocket import AsyncWebsocketClient
from yandex_music.ynison.models import ynison_state

_SESSION_SETTLE_SEC = 0.3
_SESSION_CLEANUP_TIMEOUT = 2.0


async def _cancel_and_wait(task: 'asyncio.Task[None]') -> None:
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


class YnisonClientAsync(_YnisonClientBase):
    """Асинхронный клиент Ynison.

    Асинхронный websocket-клиент для подписки на состояние плеера и отправки
    команд управления. По интерфейсу совпадает с синхронным
    :class:`yandex_music.ynison.YnisonClient`: все ключевые операции возвращают
    корутины.

    Для разовых сценариев используйте :mod:`yandex_music.ynison.simple_async`
    или контекстный менеджер :meth:`session`.

    Note:
        Интерфейс рассчитан на опытных разработчиков, знакомых с работой
        websocket-подобных долгоживущих соединений. Нужно самостоятельно
        управлять фоновой задачей :meth:`connect`, обрабатывать переподключения,
        возможные ошибки receive-loop'а и вовремя вызывать :meth:`disconnect`.
        Если нужны типовые операции (получить текущий трек, поставить паузу,
        переключить трек) — используйте :mod:`yandex_music.ynison.simple_async`.

    Attributes:
        latest_state: Последний полученный фрейм состояния.
        device_id: Идентификатор этого клиента в Ynison-сессии.
    """

    def __init__(self, token: str, device_id: Optional[str] = None) -> None:
        """Создаёт клиента. Подключение выполняется await'ом :meth:`connect`.

        Args:
            token: OAuth-токен Yandex Music.
            device_id: Идентификатор этого клиента в Ynison-сессии.
                По умолчанию случайный, но его стоит фиксировать иначе будет много клиентов.
        """
        super().__init__(token, device_id)
        self._redirect_client = AsyncWebsocketClient(
            method=self._REDIRECT_SERVICE,
            base_uri=self._BASE_URL,
            headers=self._get_redirect_headers(),
            subprotocols=self._get_subprotocols(),
        )
        self._state_client: Optional[AsyncWebsocketClient] = None

    def _init_state_client(self) -> None:
        assert self._redirect_response is not None
        self._state_client = AsyncWebsocketClient(
            method=self._STATE_SERVICE,
            base_uri=f'wss://{self._redirect_response.host}',
            headers=self._get_redirect_headers(),
            subprotocols=self._get_subprotocols(),
        )

    async def _process_redirect_message(self, message: str) -> None:
        self._handle_redirect_frame(message)
        await self._redirect_client.stop()
        self._init_state_client()

    async def _on_state_message(self, message: str) -> None:
        response = self._parse_state_frame(message)
        for listener in list(self._state_listeners):
            result = listener(response)
            if inspect.isawaitable(result):
                await result

    async def _on_state_client_connect(self) -> None:
        await self.send(messages.get_update_full_state_request(self._device_id))

    async def connect(self) -> None:
        """Корутина цикла подключения.

        Последовательно: редиректный websocket → state websocket → receive-loop
        на входящие фреймы. Возвращает управление только после
        :meth:`disconnect` (или фатальной ошибки).

        Пример:
            >>> import asyncio
            >>> client = YnisonClientAsync(token)
            >>> task = asyncio.create_task(client.connect())
        """
        await self._redirect_client.start(self._process_redirect_message)

        # если `disconnect()` вызвали до первого ответа — state_client не инициализирован
        if self._state_client is None:
            return

        await self._state_client.start(
            on_message_callback=self._on_state_message,
            on_connect_callback=self._on_state_client_connect,
        )

    async def disconnect(self) -> None:
        """Останавливает websocket.

        Корутина :meth:`connect` завершится в ближайшем receive-цикле.
        Повторный вызов — no-op.
        """
        await self._redirect_client.stop()
        if self._state_client is not None:
            await self._state_client.stop()

    async def send(self, request: ynison_state.PutYnisonStateRequest) -> None:
        """Отправляет запрос по state websocket'у.

        Args:
            request: Готовый :class:`PutYnisonStateRequest`; обычно собирается
                через билдеры из :mod:`yandex_music.ynison.messages`.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Если state websocket ещё не подключён.
        """
        if self._state_client is None:
            raise YnisonError('Клиент состояния не подключён; сначала вызовите connect()')
        await self._state_client.send(request.to_json())

    @contextlib.asynccontextmanager
    async def session(self, timeout: float = 10.0) -> AsyncIterator['YnisonClientAsync']:
        """Асинхронный контекстный менеджер для разового подключения.

        Запускает :meth:`connect` как :class:`asyncio.Task`, ждёт первый фрейм
        состояния и отдаёт клиента с заполненным :attr:`latest_state`. По выходу
        из блока вызывает :meth:`disconnect` и дожидается завершения задачи.

        Args:
            timeout: Максимальное время ожидания начального фрейма, в секундах.

        Yields:
            :obj:`yandex_music.ynison.YnisonClientAsync`: Этот же клиент, уже с загруженным состоянием.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
        """
        ready = asyncio.Event()
        self.on_state(lambda _s: ready.set())
        task: 'asyncio.Task[None]' = asyncio.create_task(self.connect())

        try:
            await asyncio.wait_for(ready.wait(), timeout=timeout)
        except asyncio.TimeoutError as exc:
            await self.disconnect()
            await _cancel_and_wait(task)
            raise YnisonError(f'Превышено время ожидания начального состояния ({timeout}с)') from exc

        try:
            yield self
            await asyncio.sleep(_SESSION_SETTLE_SEC)
        finally:
            await self.disconnect()
            try:
                await asyncio.wait_for(task, timeout=_SESSION_CLEANUP_TIMEOUT)
            except asyncio.TimeoutError:
                await _cancel_and_wait(task)
