"""Синхронный клиент Ynison."""

import contextlib
import inspect
import threading
from typing import Callable, Iterator, List, Optional

from yandex_music.exceptions import (
    YnisonConnectionClosedError,
    YnisonError,
    YnisonTimeoutError,
)
from yandex_music.ynison import _transport, messages
from yandex_music.ynison._base import _YnisonClientBase, is_terminal_error, logger
from yandex_music.ynison.models import ynison_state
from yandex_music.ynison.models.ynison_redirect import RedirectResponse

StateListener = Callable[[ynison_state.PutYnisonStateResponse], None]

_SESSION_CLEANUP_TIMEOUT = 2.0


class YnisonClient(_YnisonClientBase[StateListener]):
    """Синхронный клиент Ynison.

    Блокирующий websocket-клиент для подписки на состояние плеера Яндекс Музыки
    и управления воспроизведением. Под капотом получает у сервиса редиректа
    персональный хост и держит к нему постоянное соединение. При обрыве
    соединения клиент сам переподключается (каждый раз заново проходя редирект),
    выдерживая паузы, которые рекомендует сервер.

    Для разовых сценариев используйте контекстный менеджер :meth:`session`
    или функции из :mod:`yandex_music.ynison.simple`.

    Note:
        Один `device_id` может использоваться только одним живым подключением:
        новое подключение с тем же идентификатором вытесняет старое, и старое
        завершается с :class:`yandex_music.exceptions.YnisonDeviceDisplacedError`.

    Пример:
        >>> with YnisonClient(token).session() as client:
        ...     print(client.current_playable)
        ...     client.next_track()
    """

    def __init__(
        self,
        token: str,
        device_id: Optional[str] = None,
        device_title: str = messages.DEFAULT_DEVICE_TITLE,
        max_reconnect_attempts: Optional[int] = None,
    ) -> None:
        """Создаёт клиента. Подключение выполняется вызовом :meth:`connect` или :meth:`session`.

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
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._connection: Optional[_transport.SyncConnection] = None
        self._redirect_connection: Optional[_transport.SyncConnection] = None

    def on_state(self, listener: StateListener) -> StateListener:
        """Регистрирует listener, вызываемый на каждый фрейм состояния.

        Можно использовать как декоратор. Listener вызывается из потока receive-loop'а.
        Исключения listener'а логируются в логгер `yandex_music.ynison` и не прерывают приём фреймов.

        Args:
            listener: Синхронный callable, принимающий
                :class:`yandex_music.ynison.models.ynison_state.PutYnisonStateResponse`.

        Returns:
            Тот же listener (для удобства использования как декоратор).

        Raises:
            :class:`TypeError`: Если передана корутинная функция. Для них используйте :class:`YnisonClientAsync`.
        """
        if inspect.iscoroutinefunction(listener):
            raise TypeError("YnisonClient не поддерживает асинхронные listener'ы; используйте YnisonClientAsync")
        return super().on_state(listener)

    def _begin(self) -> None:
        with self._lock:
            if self._running:
                raise YnisonError('Клиент уже подключён; вызовите disconnect() перед повторным подключением')
            self._running = True
            self._stop.clear()
            self._reset_connection_state()

    def _end(self) -> None:
        with self._lock:
            self._running = False
            self._connection = None
            self._redirect_connection = None

    def connect(self) -> None:
        """Блокирующий цикл подключения.

        Получает редирект, подключается к state-хосту и обрабатывает входящие фреймы.
        При потере соединения переподключается. Возвращает управление после :meth:`disconnect`.

        Пример:
            >>> client = YnisonClient(token)
            >>> threading.Thread(target=client.connect, daemon=True).start()

        Raises:
            :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
            :class:`yandex_music.exceptions.YnisonDeviceDisplacedError`: Подключился другой клиент
                с тем же `device_id`.
            :class:`yandex_music.exceptions.YnisonError`: Клиент уже запущен, или превышен
                `max_reconnect_attempts` (выбрасывается последняя ошибка соединения).
        """
        self._begin()
        try:
            self._run()
        finally:
            self._end()

    def disconnect(self) -> None:
        """Останавливает подключение.

        :meth:`connect` вернёт управление в ближайшее время. Повторный вызов ничего не делает.
        После отключения клиента можно подключить заново.
        """
        with self._lock:
            if not self._running:
                return
            self._stop.set()
            connections = [self._redirect_connection, self._connection]

        for connection in connections:
            if connection is not None:
                with contextlib.suppress(Exception):
                    connection.close()

    @contextlib.contextmanager
    def session(self, timeout: float = 10.0) -> Iterator['YnisonClient']:
        """Контекстный менеджер для подключения на время блока.

        Запускает :meth:`connect` в фоновом потоке, ждёт первый фрейм состояния
        и отдаёт клиента с заполненным :attr:`latest_state`. По выходу из блока
        отключается и дожидается завершения потока.

        Args:
            timeout: Максимальное время ожидания начального фрейма, в секундах.

        Yields:
            :obj:`yandex_music.ynison.YnisonClient`: Этот же клиент, уже с загруженным состоянием.

        Raises:
            :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
            :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
            :class:`yandex_music.exceptions.YnisonError`: Любая другая терминальная ошибка подключения.
        """
        self._begin()
        ready = threading.Event()
        failures: List[BaseException] = []

        def on_first_state(_state: ynison_state.PutYnisonStateResponse) -> None:
            ready.set()

        def run() -> None:
            try:
                self._run()
            except BaseException as e:  # noqa: BLE001
                failures.append(e)
            finally:
                self._end()
                ready.set()

        self._state_listeners.append(on_first_state)
        thread = threading.Thread(target=run, name='ynison-connect', daemon=True)
        thread.start()

        try:
            if not ready.wait(timeout):
                raise YnisonTimeoutError(f'Превышено время ожидания начального состояния ({timeout}с)') from (
                    self._last_error
                )
            if failures:
                raise failures[0]
            if self._latest_state is None:
                raise YnisonConnectionClosedError('Соединение закрыто до получения начального состояния')

            yield self
        finally:
            self.remove_listener(on_first_state)
            self.disconnect()
            thread.join(timeout=_SESSION_CLEANUP_TIMEOUT)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                self._serve(self._fetch_redirect())
                error: YnisonError = YnisonConnectionClosedError('Сервер закрыл соединение')
            except (YnisonError, OSError, _transport.WebSocketException) as e:
                if self._stop.is_set():
                    return
                error = self._to_reconnectable_error(e)
            if self._stop.is_set():
                return

            self._remember_error(error)
            self._emit_error(error)
            delay = self._next_reconnect_delay()
            logger.debug('Ynison: переподключение через %.2f с после ошибки: %r', delay, error)
            if self._stop.wait(delay):
                return

    def _fetch_redirect(self) -> RedirectResponse:
        connection = _transport.open_sync(self._redirect_uri(), self._get_headers(), self._get_subprotocols())
        with self._lock:
            stopped = self._stop.is_set()
            if not stopped:
                self._redirect_connection = connection
        if stopped:
            connection.close()
            raise YnisonConnectionClosedError('Клиент отключён')
        try:
            message = connection.recv(timeout=self._REDIRECT_TIMEOUT)
        except TimeoutError as e:
            raise YnisonTimeoutError('Сервис редиректа Ynison не ответил вовремя') from e
        finally:
            with self._lock:
                self._redirect_connection = None
            # close handshake редиректа идёт параллельно с подключением к state-хосту
            threading.Thread(target=connection.close, name='ynison-redirect-close', daemon=True).start()

        if not isinstance(message, str):
            raise YnisonError('Сервис редиректа Ynison прислал бинарный фрейм')
        return self._parse_redirect_frame(message)

    def _serve(self, redirect: RedirectResponse) -> None:
        ping_interval, ping_timeout = self._ping_params(redirect)
        connection = _transport.open_sync(
            self._state_uri(redirect),
            self._get_headers(),
            self._get_subprotocols(redirect),
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
        )
        with connection:
            with self._lock:
                if self._stop.is_set():
                    return
                self._connection = connection
            try:
                _transport.start_sync_keepalive(connection, ping_interval, ping_timeout)
                connection.send(self._full_state_request().to_json())
                for message in connection:
                    if isinstance(message, str):
                        self._dispatch(message)
            finally:
                with self._lock:
                    self._connection = None

    def _dispatch(self, message: str) -> None:
        try:
            state = self._parse_state_frame(message)
        except YnisonError as e:
            if is_terminal_error(e):
                raise
            self._remember_error(e)
            self._emit_error(e)
            return

        for listener in list(self._state_listeners):
            try:
                listener(state)
            except Exception:  # noqa: BLE001
                logger.exception('Ynison: исключение в state listener %r', listener)

    def _emit_error(self, error: YnisonError) -> None:
        for listener in list(self._error_listeners):
            try:
                listener(error)
            except Exception:  # noqa: BLE001
                logger.exception('Ynison: исключение в error listener %r', listener)

    def send(self, request: ynison_state.PutYnisonStateRequest) -> None:
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
            connection.send(request.to_json())
        except _transport.ConnectionClosed as e:
            raise YnisonConnectionClosedError(f'Соединение с Ynison закрыто: {e}') from e

    def pause(self) -> None:
        """Ставит воспроизведение на паузу на активном устройстве.

        Raises:
            :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если нет активного устройства.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        self.send(self._build_set_paused_request(paused=True))

    def resume(self) -> None:
        """Снимает паузу на активном устройстве.

        Raises:
            :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если нет активного устройства.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        self.send(self._build_set_paused_request(paused=False))

    def next_track(self) -> None:
        """Переключает на следующий трек в очереди (с учётом перемешивания).

        Raises:
            :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек последний.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        self.send(self._build_change_track_request(delta=1))

    def previous_track(self) -> None:
        """Переключает на предыдущий трек в очереди (с учётом перемешивания).

        Raises:
            :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек первый.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        self.send(self._build_change_track_request(delta=-1))

    def set_volume(self, volume: float, target_device_id: Optional[str] = None) -> None:
        """Устанавливает громкость на указанном или активном устройстве.

        Args:
            volume: Громкость в диапазоне [0.0; 1.0]; значения вне диапазона обрезаются.
            target_device_id: Идентификатор устройства. По умолчанию активное устройство.

        Raises:
            :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если устройство не указано
                и активного нет.
            :class:`yandex_music.exceptions.YnisonConnectionClosedError`: Если соединение закрыто.
        """
        self.send(self._build_set_volume_request(volume, target_device_id))
