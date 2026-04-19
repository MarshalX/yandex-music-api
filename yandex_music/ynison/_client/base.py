"""Базовый класс клиентов Ynison.

Содержит общую логику handshake'ов, парсинга входящих фреймов и управления
слушателями. Не предназначен для прямого использования — см. публичные
:class:`yandex_music.ynison.YnisonClient` и :class:`yandex_music.ynison.YnisonClientAsync`.
"""

import contextlib
import urllib.parse
from typing import Any, Awaitable, Callable, List, Optional, Union

from yandex_music.exceptions import YnisonError
from yandex_music.utils import json_compat
from yandex_music.ynison import messages
from yandex_music.ynison.models import ynison_state
from yandex_music.ynison.models.ynison_redirect import RedirectResponse

StateListener = Callable[[ynison_state.PutYnisonStateResponse], Union[None, Awaitable[None]]]


class _YnisonClientBase:
    """Базовый класс sync- и async-клиентов Ynison.

    Владеет токеном, device_id, последним полученным состоянием и списком
    слушателей. Транспортные операции (:meth:`send`, :meth:`disconnect`)
    абстрактны и переопределяются в подклассах.
    """

    _BASE_URL = 'wss://ynison.music.yandex.ru'
    _REDIRECT_SERVICE = 'redirector.YnisonRedirectService/GetRedirectToYnison'
    _STATE_SERVICE = 'ynison_state.YnisonStateService/PutYnisonState'
    _KEEPALIVE_PING_INTERVAL = 20

    def __init__(self, token: str, device_id: Optional[str] = None) -> None:
        """Инициализация базового клиента.

        Args:
            token: OAuth-токен Yandex Music.
            device_id: Идентификатор этого клиента в Ynison-сессии. По умолчанию — случайный.
        """
        self._token = token
        self._device_id = device_id or messages.generate_device_id()
        self._redirect_response: Optional[RedirectResponse] = None
        self._latest_state: Optional[ynison_state.PutYnisonStateResponse] = None
        self._state_listeners: List[StateListener] = []

    @property
    def latest_state(self) -> Optional[ynison_state.PutYnisonStateResponse]:
        """Последний полученный фрейм состояния.

        Returns:
            :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateResponse` | :obj:`None`:
                Самый свежий фрейм от сервера или :obj:`None`, если фреймы ещё не приходили.
        """
        return self._latest_state

    @property
    def device_id(self) -> str:
        """Идентификатор этого клиента в Ynison-сессии.

        Returns:
            :obj:`str`: Идентификатор устройства, переданный в конструктор или сгенерированный автоматически.
        """
        return self._device_id

    def _require_state(self) -> ynison_state.PutYnisonStateResponse:
        if self._latest_state is None:
            raise YnisonError('Состояние ещё не получено; дождитесь первого фрейма от сервера перед отправкой команд')
        return self._latest_state

    def _get_device_info(self) -> str:
        device_info = {
            'Ynison-Device-Id': self._device_id,
            # да, они реально тут хотят вложенный json.dumps иначе не работает
            'Ynison-Device-Info': json_compat.dumps(
                {
                    'app_name': 'Python SDK',
                    'type': '1',  # 1 — браузеры
                }
            ),
        }
        if self._redirect_response:
            device_info['Ynison-Redirect-Ticket'] = self._redirect_response.redirect_ticket
            device_info['Ynison-Session-Id'] = str(self._redirect_response.session_id)
        return json_compat.dumps(device_info)

    def _get_subprotocols(self) -> List[str]:
        return ['Bearer', 'v2', urllib.parse.quote(self._get_device_info())]

    def _get_redirect_headers(self) -> dict:
        return {
            'Origin': 'https://music.yandex.ru',  # важно
            'Authorization': f'OAuth {self._token}',  # ещё важнее
        }

    def _handle_redirect_frame(self, message: str) -> RedirectResponse:
        assert self._redirect_response is None, 'Редирект уже получен'
        response = RedirectResponse().from_json(message)
        if not (response.redirect_ticket and response.session_id and response.host):
            raise ValueError(message)
        self._redirect_response = response
        return response

    def _parse_state_frame(self, message: str) -> ynison_state.PutYnisonStateResponse:
        response = ynison_state.PutYnisonStateResponse().from_json(message)
        self._latest_state = response
        return response

    def on_state(self, listener: StateListener) -> StateListener:
        """Регистрирует listener, вызываемый на каждый фрейм состояния.

        Можно использовать как декоратор. Возвращает переданный listener без изменений.
        Listener вызывается из потока receive-loop (sync) или из event loop'а (async).

        Args:
            listener: Callable, принимающий :class:`PutYnisonStateResponse`. Может быть синхронным
                или асинхронным; асинхронные await'ятся только в :class:`YnisonClientAsync`.

        Returns:
            :obj:`StateListener`: Тот же listener (для удобства использования как декоратор).
        """
        self._state_listeners.append(listener)
        return listener

    def remove_listener(self, listener: StateListener) -> None:
        """Удаляет ранее зарегистрированный listener.

        Args:
            listener: Listener, ранее переданный в :meth:`on_state`.
                Если listener не зарегистрирован — вызов тихо игнорируется.
        """
        with contextlib.suppress(ValueError):
            self._state_listeners.remove(listener)

    def send(self, request: ynison_state.PutYnisonStateRequest) -> Any:
        """Отправляет произвольный `PutYnisonStateRequest` по state websocket'у.

        Args:
            request: Готовый запрос, обычно собранный одним из билдеров
                из :mod:`yandex_music.ynison.messages`.

        Returns:
            :obj:`None` в :class:`YnisonClient`; :class:`Coroutine` в :class:`YnisonClientAsync`.

        Raises:
            NotImplementedError: На базовом классе; реализуется в подклассах.
        """
        raise NotImplementedError

    def disconnect(self) -> Any:
        """Закрывает websocket-соединения.

        Вызов инициирует остановку receive-loop'ов; блокирующий `connect()`
        вернёт управление вскоре после этого.

        Returns:
            :obj:`None` в :class:`YnisonClient`; :class:`Coroutine` в :class:`YnisonClientAsync`.

        Raises:
            NotImplementedError: На базовом классе; реализуется в подклассах.
        """
        raise NotImplementedError
