"""Синхронный клиент Ynison."""

import contextlib
import threading
import time
from typing import Iterator, Optional

from yandex_music.exceptions import YnisonError
from yandex_music.ynison import messages
from yandex_music.ynison._client.base import _YnisonClientBase
from yandex_music.ynison._websocket import WebsocketClient
from yandex_music.ynison.models import ynison_state

_SESSION_SETTLE_SEC = 0.3
_SESSION_CLEANUP_TIMEOUT = 2.0


class YnisonClient(_YnisonClientBase):
    """Синхронный клиент Ynison.

    Блокирующий websocket-клиент для подписки на состояние плеера Яндекс Музыки
    и отправки команд управления. Под капотом открывает два websocket-соединения:
    сначала к сервису редиректа, затем к персональному хосту Ynison.

    Для разовых сценариев «открыть соединение → сделать одно действие → закрыть»
    используйте :mod:`yandex_music.ynison.simple` или контекстный менеджер
    :meth:`session`.

    Note:
        Интерфейс рассчитан на опытных разработчиков, знакомых с работой
        websocket-подобных долгоживущих соединений. Нужно самостоятельно
        управлять фоновым потоком :meth:`connect`, обрабатывать переподключения,
        возможные ошибки receive-loop'а и вовремя вызывать :meth:`disconnect`.
        Если нужны типовые операции (получить текущий трек, поставить паузу,
        переключить трек) — используйте :mod:`yandex_music.ynison.simple`.

    Attributes:
        latest_state: Последний полученный фрейм состояния.
        device_id: Идентификатор этого клиента в Ynison-сессии.
    """

    def __init__(self, token: str, device_id: Optional[str] = None) -> None:
        """Создаёт клиента. Подключение выполняется вызовом :meth:`connect`.

        Args:
            token: OAuth-токен Yandex Music.
            device_id: Идентификатор этого клиента в Ynison-сессии.
                По умолчанию случайный, но его стоит фиксировать иначе будет много клиентов.
        """
        super().__init__(token, device_id)
        self._keepalive_thread: Optional[threading.Thread] = None
        self._keepalive_stop = threading.Event()
        self._redirect_client = WebsocketClient(
            method=self._REDIRECT_SERVICE,
            base_uri=self._BASE_URL,
            headers=self._get_redirect_headers(),
            subprotocols=self._get_subprotocols(),
        )
        self._state_client: Optional[WebsocketClient] = None

    def _init_state_client(self) -> None:
        assert self._redirect_response is not None
        self._state_client = WebsocketClient(
            method=self._STATE_SERVICE,
            base_uri=f'wss://{self._redirect_response.host}',
            headers=self._get_redirect_headers(),
            subprotocols=self._get_subprotocols(),
        )

    def _process_redirect_message(self, message: str) -> None:
        self._handle_redirect_frame(message)
        self._redirect_client.stop()
        self._init_state_client()

    def _on_state_client_connect(self) -> None:
        self.send(messages.get_update_full_state_request(self._device_id))
        self._start_keepalive()

    def _on_state_message(self, message: str) -> None:
        response = self._parse_state_frame(message)
        for listener in list(self._state_listeners):
            listener(response)

    def connect(self) -> None:
        """Блокирующий цикл подключения.

        Последовательно: редиректный websocket → state websocket → receive-loop
        на входящие фреймы. Возвращает управление только после вызова
        :meth:`disconnect` (или фатальной ошибки соединения).

        Пример:
            >>> import threading
            >>> client = YnisonClient(token)
            >>> threading.Thread(target=client.connect, daemon=True).start()
        """
        # блокируемся до получения билета
        self._redirect_client.start(self._process_redirect_message)

        # если `disconnect()` вызвали до первого ответа — state_client не инициализирован
        if self._state_client is None:
            return

        self._state_client.start(
            on_message_callback=self._on_state_message,
            on_connect_callback=self._on_state_client_connect,
        )

    def disconnect(self) -> None:
        """Останавливает websocket.

        Блокирующий :meth:`connect` вернёт управление в ближайшем receive-цикле.
        Повторный вызов — no-op.
        """
        self._keepalive_stop.set()
        self._redirect_client.stop()
        if self._state_client is not None:
            self._state_client.stop()

    def send(self, request: ynison_state.PutYnisonStateRequest) -> None:
        """Отправляет запрос по state websocket'у.

        Args:
            request: Готовый :class:`PutYnisonStateRequest`; обычно собирается
                через билдеры из :mod:`yandex_music.ynison.messages`.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Если state websocket ещё не подключён.
        """
        if self._state_client is None:
            raise YnisonError('Клиент состояния не подключён; сначала вызовите connect()')
        self._state_client.send(request.to_json())

    @contextlib.contextmanager
    def session(self, timeout: float = 10.0) -> Iterator['YnisonClient']:
        """Контекстный менеджер для разового подключения.

        Запускает :meth:`connect` в daemon-потоке, ждёт первый фрейм состояния
        и отдаёт клиента с заполненным :attr:`latest_state`. По выходу из блока
        вызывает :meth:`disconnect` и дожидается завершения потока.

        Args:
            timeout: Максимальное время ожидания начального фрейма, в секундах.

        Yields:
            :obj:`yandex_music.ynison.YnisonClient`: Этот же клиент, уже с загруженным состоянием.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
        """
        ready = threading.Event()
        self.on_state(lambda _s: ready.set())
        thread = threading.Thread(target=self.connect, daemon=True)
        thread.start()

        if not ready.wait(timeout=timeout):
            self.disconnect()
            thread.join(timeout=_SESSION_CLEANUP_TIMEOUT)
            raise YnisonError(f'Превышено время ожидания начального состояния ({timeout}с)')

        try:
            yield self
            time.sleep(_SESSION_SETTLE_SEC)  # дать серверу применить последнюю команду
        finally:
            self.disconnect()
            thread.join(timeout=_SESSION_CLEANUP_TIMEOUT)

    def _keepalive_worker(self) -> None:
        while not self._keepalive_stop.is_set():
            if self._state_client is None:
                return
            try:
                self._state_client.send_ping()
            except Exception:  # noqa: BLE001 -- соединение уже закрыто, выходим молча
                return

            if self._keepalive_stop.wait(timeout=self._KEEPALIVE_PING_INTERVAL):
                return

    def _start_keepalive(self) -> None:
        # защита от дубликата потока при переподключении state websocket'а
        if self._keepalive_thread is not None and self._keepalive_thread.is_alive():
            return
        self._keepalive_stop.clear()
        self._keepalive_thread = threading.Thread(target=self._keepalive_worker, daemon=True)
        self._keepalive_thread.start()
