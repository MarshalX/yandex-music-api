"""Асинхронный клиент Ynison."""

import asyncio
import contextlib
import inspect
from typing import AsyncIterator, Awaitable, Callable, Optional, Set, Union

from yandex_music.exceptions import (
    YnisonConnectionClosedError,
    YnisonError,
    YnisonTimeoutError,
)
from yandex_music.ynison import _transport, messages
from yandex_music.ynison._base import _YnisonClientBase, is_terminal_error, logger
from yandex_music.ynison.models import ynison_state
from yandex_music.ynison.models.ynison_redirect import RedirectResponse

AsyncStateListener = Callable[[ynison_state.PutYnisonStateResponse], Union[None, Awaitable[None]]]

_SESSION_CLEANUP_TIMEOUT = 2.0


async def _close_connection(connection: _transport.AsyncConnection) -> None:
    try:
        await connection.close()
    finally:
        # иначе asyncio пишет `unclosed transport`, если loop завершится раньше SSL shutdown
        connection.transport.abort()


class YnisonClientAsync(_YnisonClientBase[AsyncStateListener]):
    """Асинхронный клиент Ynison.

    Асинхронный аналог :class:`yandex_music.ynison.YnisonClient` с тем же
    интерфейсом: все операции ввода-вывода являются корутинами. При обрыве соединения
    клиент сам переподключается (каждый раз заново проходя редирект).

    Для разовых сценариев используйте асинхронный контекстный менеджер :meth:`session`
    или функции из :mod:`yandex_music.ynison.simple_async`.

    Note:
        Один `device_id` может использоваться только одним живым подключением:
        новое подключение с тем же идентификатором вытесняет старое, и старое
        завершается с :class:`yandex_music.exceptions.YnisonDeviceDisplacedError`.

    Note:
        Listener'ы состояния вызываются последовательно внутри receive-loop'а, чтобы
        сохранить порядок фреймов. Долгие операции в listener'е задерживают приём
        следующих фреймов, поэтому выносите их в отдельные задачи.

    Пример:
        >>> async with YnisonClientAsync(token).session() as client:
        ...     print(client.current_playable)
        ...     await client.next_track()
    """

    def __init__(
        self,
        token: str,
        device_id: Optional[str] = None,
        device_title: str = messages.DEFAULT_DEVICE_TITLE,
        max_reconnect_attempts: Optional[int] = None,
    ) -> None:
        """Создаёт клиента. Подключение выполняется await'ом :meth:`connect` или через :meth:`session`.

        Клиента можно создавать вне запущенного event loop'а: asyncio-примитивы
        создаются при подключении.

        Args:
            token: OAuth-токен Yandex Music.
            device_id: Идентификатор этого клиента в Ynison-сессии. По умолчанию
                детерминированный, вычисленный из токена, чтобы повторные запуски
                не плодили новые устройства.
            device_title: Название устройства, которое увидят другие клиенты.
            max_reconnect_attempts: Сколько подряд неудачных переподключений допускается,
                прежде чем :meth:`connect` завершится ошибкой. :obj:`None` означает без ограничения.
        """
        super().__init__(token, device_id, device_title, max_reconnect_attempts)
        self._stop: Optional[asyncio.Event] = None
        self._connection: Optional[_transport.AsyncConnection] = None
        self._redirect_connection: Optional[_transport.AsyncConnection] = None
        self._background_tasks: Set['asyncio.Task[None]'] = set()

    def on_state(self, listener: AsyncStateListener) -> AsyncStateListener:
        """Регистрирует listener, вызываемый на каждый фрейм состояния.

        Можно использовать как декоратор. Listener может быть синхронным или асинхронным.
        Исключения listener'а логируются в логгер `yandex_music.ynison` и не прерывают приём фреймов.

        Args:
            listener: Callable, принимающий
                :class:`yandex_music.ynison.models.ynison_state.PutYnisonStateResponse`.

        Returns:
            Тот же listener (для удобства использования как декоратор).
        """
        return super().on_state(listener)

    def _begin(self) -> asyncio.Event:
        if self._running:
            raise YnisonError('Клиент уже подключён; вызовите disconnect() перед повторным подключением')
        self._running = True
        self._stop = asyncio.Event()
        self._reset_connection_state()
        return self._stop

    async def _end(self) -> None:
        self._running = False
        self._connection = None
        self._redirect_connection = None
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

    async def connect(self) -> None:
        """Корутина цикла подключения.

        Получает редирект, подключается к state-хосту и обрабатывает входящие фреймы.
        При потере соединения переподключается. Завершается после :meth:`disconnect`.

        Пример:
            >>> client = YnisonClientAsync(token)
            >>> task = asyncio.create_task(client.connect())

        Raises:
            :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
            :class:`yandex_music.exceptions.YnisonDeviceDisplacedError`: Подключился другой клиент
                с тем же `device_id`.
            :class:`yandex_music.exceptions.YnisonError`: Клиент уже запущен, или превышен
                `max_reconnect_attempts` (выбрасывается последняя ошибка соединения).
        """
        stop = self._begin()
        try:
            await self._run(stop)
        finally:
            await self._end()

    async def disconnect(self) -> None:
        """Останавливает подключение.

        Корутина :meth:`connect` завершится в ближайшее время. Повторный вызов ничего не делает.
        После отключения клиента можно подключить заново.
        """
        if not self._running or self._stop is None:
            return
        self._stop.set()
        for connection in (self._redirect_connection, self._connection):
            if connection is not None:
                with contextlib.suppress(Exception):
                    await connection.close()

    @contextlib.asynccontextmanager
    async def session(self, timeout: float = 10.0) -> AsyncIterator['YnisonClientAsync']:
        """Асинхронный контекстный менеджер для подключения на время блока.

        Запускает :meth:`connect` как :class:`asyncio.Task`, ждёт первый фрейм
        состояния и отдаёт клиента с заполненным :attr:`latest_state`. По выходу
        из блока отключается и дожидается завершения задачи.

        Args:
            timeout: Максимальное время ожидания начального фрейма, в секундах.

        Yields:
            :obj:`yandex_music.ynison.YnisonClientAsync`: Этот же клиент, уже с загруженным состоянием.

        Raises:
            :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
            :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
            :class:`yandex_music.exceptions.YnisonError`: Любая другая терминальная ошибка подключения.
        """
        stop = self._begin()
        ready = asyncio.Event()

        def on_first_state(_state: ynison_state.PutYnisonStateResponse) -> None:
            ready.set()

        async def run() -> None:
            try:
                await self._run(stop)
            finally:
                await self._end()

        self._state_listeners.append(on_first_state)
        task = asyncio.ensure_future(run())
        waiter = asyncio.ensure_future(ready.wait())

        try:
            done, _ = await asyncio.wait({task, waiter}, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
            if not done:
                raise YnisonTimeoutError(f'Превышено время ожидания начального состояния ({timeout}с)') from (
                    self._last_error
                )
            if task in done:
                task.result()  # пробрасывает терминальную ошибку подключения
                if self._latest_state is None:
                    raise YnisonConnectionClosedError('Соединение закрыто до получения начального состояния')

            yield self
        finally:
            waiter.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await waiter
            self.remove_listener(on_first_state)
            await self.disconnect()
            _, pending = await asyncio.wait({task}, timeout=_SESSION_CLEANUP_TIMEOUT)
            for leftover in pending:
                leftover.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task

    async def _run(self, stop: asyncio.Event) -> None:
        while not stop.is_set():
            try:
                await self._serve(await self._fetch_redirect(stop), stop)
                error: YnisonError = YnisonConnectionClosedError('Сервер закрыл соединение')
            except (YnisonError, OSError, asyncio.TimeoutError, _transport.WebSocketException) as e:
                if stop.is_set():
                    return
                error = self._to_reconnectable_error(e)
            if stop.is_set():
                return

            self._remember_error(error)
            await self._emit_error(error)
            delay = self._next_reconnect_delay()
            logger.debug('Ynison: переподключение через %.2f с после ошибки: %r', delay, error)
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(stop.wait(), timeout=delay)

    async def _fetch_redirect(self, stop: asyncio.Event) -> RedirectResponse:
        connection = await _transport.open_async(self._redirect_uri(), self._get_headers(), self._get_subprotocols())
        if stop.is_set():
            await connection.close()
            raise YnisonConnectionClosedError('Клиент отключён')

        self._redirect_connection = connection
        try:
            message = await asyncio.wait_for(connection.recv(), timeout=self._REDIRECT_TIMEOUT)
        except asyncio.TimeoutError as e:
            raise YnisonTimeoutError('Сервис редиректа Ynison не ответил вовремя') from e
        finally:
            self._redirect_connection = None
            # close handshake редиректа идёт параллельно с подключением к state-хосту
            close_task = asyncio.ensure_future(_close_connection(connection))
            self._background_tasks.add(close_task)
            close_task.add_done_callback(self._background_tasks.discard)

        if not isinstance(message, str):
            raise YnisonError('Сервис редиректа Ynison прислал бинарный фрейм')
        return self._parse_redirect_frame(message)

    async def _serve(self, redirect: RedirectResponse, stop: asyncio.Event) -> None:
        ping_interval, ping_timeout = self._ping_params(redirect)
        connection = await _transport.open_async(
            self._state_uri(redirect),
            self._get_headers(),
            self._get_subprotocols(redirect),
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
        )
        async with connection:
            if stop.is_set():
                return
            self._connection = connection
            try:
                await connection.send(self._full_state_request().to_json())
                async for message in connection:
                    if isinstance(message, str):
                        await self._dispatch(message)
            finally:
                self._connection = None

    async def _dispatch(self, message: str) -> None:
        try:
            state = self._parse_state_frame(message)
        except YnisonError as e:
            if is_terminal_error(e):
                raise
            self._remember_error(e)
            await self._emit_error(e)
            return

        for listener in list(self._state_listeners):
            try:
                result = listener(state)
                if inspect.isawaitable(result):
                    await result
            except Exception:  # noqa: BLE001
                logger.exception('Ynison: исключение в state listener %r', listener)

    async def _emit_error(self, error: YnisonError) -> None:
        for listener in list(self._error_listeners):
            try:
                result = listener(error)
                if inspect.isawaitable(result):
                    await result
            except Exception:  # noqa: BLE001
                logger.exception('Ynison: исключение в error listener %r', listener)

    async def send(self, request: ynison_state.PutYnisonStateRequest) -> None:
        """Отправляет произвольный запрос по state websocket'у.

        Args:
            request: Готовый :class:`PutYnisonStateRequest`; обычно собирается
                через билдеры из :mod:`yandex_music.ynison.messages`.

        Raises:
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединения нет или оно закрыто.
        """
        connection = self._connection
        if connection is None:
            raise self._no_connection_error()
        try:
            await connection.send(request.to_json())
        except _transport.ConnectionClosed as e:
            raise YnisonConnectionClosedError(f'Соединение с Ynison закрыто: {e}') from e

    async def pause(self) -> None:
        """Ставит воспроизведение на паузу на активном устройстве.

        Raises:
            :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если нет активного устройства.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        await self.send(self._build_set_paused_request(paused=True))

    async def resume(self) -> None:
        """Снимает паузу на активном устройстве.

        Raises:
            :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если нет активного устройства.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        await self.send(self._build_set_paused_request(paused=False))

    async def next_track(self) -> None:
        """Переключает на следующий трек в очереди (с учётом перемешивания).

        Raises:
            :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек последний.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        await self.send(self._build_change_track_request(delta=1))

    async def previous_track(self) -> None:
        """Переключает на предыдущий трек в очереди (с учётом перемешивания).

        Raises:
            :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек первый.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        await self.send(self._build_change_track_request(delta=-1))

    async def set_volume(self, volume: float, target_device_id: Optional[str] = None) -> None:
        """Устанавливает громкость на указанном или активном устройстве.

        Args:
            volume: Громкость в диапазоне [0.0; 1.0]; значения вне диапазона обрезаются.
            target_device_id: Идентификатор устройства. По умолчанию активное устройство.

        Raises:
            :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если устройство не указано
                и активного нет.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        await self.send(self._build_set_volume_request(volume, target_device_id))
