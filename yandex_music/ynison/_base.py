"""Общая часть sync- и async-клиентов Ynison.

Handshake-заголовки, разбор фреймов (включая error-фреймы сервера), слушатели,
политика переподключений и сборка команд управления из последнего состояния.
"""

import logging
import random
import urllib.parse
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar

from yandex_music.exceptions import (
    YnisonConnectionClosedError,
    YnisonDeviceDisplacedError,
    YnisonError,
    YnisonNoActiveDeviceError,
    YnisonServerError,
    YnisonUnauthorizedError,
)
from yandex_music.utils import json_compat
from yandex_music.ynison import _transport, messages, utils
from yandex_music.ynison.models import ynison_state
from yandex_music.ynison.models.ynison_redirect import RedirectResponse

logger = logging.getLogger('yandex_music.ynison')
logger.addHandler(logging.NullHandler())

ErrorListener = Callable[[YnisonError], Any]
ListenerT = TypeVar('ListenerT', bound=Callable[..., Any])

_GRPC_UNAUTHENTICATED = 16
_GRPC_PERMISSION_DENIED = 7
_ERROR_CODE_DEVICE_DISPLACED = '400090001'
# Такую же лестницу присылает сервер в `ynison-backoff-millis`.
_DEFAULT_BACKOFF_MS = [0, 1000, 5000, 30000]
_DEFAULT_PING_INTERVAL = 20.0
_DEFAULT_PING_TIMEOUT = 20.0


def _parse_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_backoff(value: Any) -> List[int]:
    if not isinstance(value, str):
        return []
    result = [_parse_int(part) for part in value.split(':')]
    return [part for part in result if part is not None]


def parse_server_error(payload: Dict[str, Any]) -> YnisonServerError:
    """Превращает error-фрейм сервера в исключение подходящего класса.

    Args:
        payload: Содержимое ключа `error` из JSON-фрейма.

    Returns:
        :class:`yandex_music.exceptions.YnisonServerError`: Исключение (не выброшенное).
    """
    details = payload.get('details') or payload.get('extra_headers') or {}
    if not isinstance(details, dict):
        details = {}

    kwargs = {
        'message': str(payload.get('message') or 'Неизвестная ошибка Ynison'),
        'grpc_code': _parse_int(payload.get('grpc_code')),
        'http_code': _parse_int(payload.get('http_code')),
        'error_code': details.get('ynison-error-code'),
        'backoff_ms': _parse_backoff(details.get('ynison-backoff-millis')),
        'go_away_seconds': _parse_int(details.get('ynison-go-away-for-seconds')),
    }

    if kwargs['grpc_code'] in (_GRPC_UNAUTHENTICATED, _GRPC_PERMISSION_DENIED) or kwargs['http_code'] in (401, 403):
        return YnisonUnauthorizedError(**kwargs)
    if kwargs['error_code'] == _ERROR_CODE_DEVICE_DISPLACED:
        return YnisonDeviceDisplacedError(**kwargs)
    return YnisonServerError(**kwargs)


def is_terminal_error(error: YnisonError) -> bool:
    """Проверяет, что после ошибки переподключаться бессмысленно.

    Терминальные: ошибка аутентификации, вытеснение другим клиентом
    и любые ошибки, для которых сервер просит не возвращаться (`go_away`).
    """
    if isinstance(error, (YnisonUnauthorizedError, YnisonDeviceDisplacedError)):
        return True
    return isinstance(error, YnisonServerError) and bool(error.go_away_seconds)


class _YnisonClientBase(Generic[ListenerT]):
    """Базовый класс sync- и async-клиентов Ynison. Не предназначен для прямого использования."""

    _BASE_URL = 'wss://ynison.music.yandex.ru'
    _REDIRECT_SERVICE = 'redirector.YnisonRedirectService/GetRedirectToYnison'
    _STATE_SERVICE = 'ynison_state.YnisonStateService/PutYnisonState'
    _REDIRECT_TIMEOUT = 10.0

    def __init__(
        self,
        token: str,
        device_id: Optional[str] = None,
        device_title: str = messages.DEFAULT_DEVICE_TITLE,
        max_reconnect_attempts: Optional[int] = None,
    ) -> None:
        """Инициализация базового клиента.

        Args:
            token: OAuth-токен Yandex Music.
            device_id: Идентификатор этого клиента в Ynison-сессии. По умолчанию
                детерминированный, вычисленный из токена.
            device_title: Название устройства, которое увидят другие клиенты.
            max_reconnect_attempts: Сколько подряд неудачных переподключений допускается,
                прежде чем :meth:`connect` завершится ошибкой. :obj:`None` означает без ограничения.
        """
        self._token = token
        self._device_id = device_id or messages.generate_device_id(seed=f'yandex-music-ynison:{token}')
        self._device_title = device_title
        self._max_reconnect_attempts = max_reconnect_attempts

        self._redirect_response: Optional[RedirectResponse] = None
        self._latest_state: Optional[ynison_state.PutYnisonStateResponse] = None
        self._last_error: Optional[YnisonError] = None
        self._state_listeners: List[ListenerT] = []
        self._error_listeners: List[ErrorListener] = []

        self._running = False
        self._reconnect_attempt = 0
        self._backoff_ms = list(_DEFAULT_BACKOFF_MS)

    @property
    def latest_state(self) -> Optional[ynison_state.PutYnisonStateResponse]:
        """Последний полученный фрейм состояния или :obj:`None`, если фреймов ещё не было."""
        return self._latest_state

    @property
    def state(self) -> ynison_state.PutYnisonStateResponse:
        """Последний полученный фрейм состояния.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Если состояние ещё не получено.
        """
        if self._latest_state is None:
            raise YnisonError('Состояние ещё не получено; дождитесь первого фрейма от сервера')
        return self._latest_state

    @property
    def device_id(self) -> str:
        """Идентификатор этого клиента в Ynison-сессии."""
        return self._device_id

    @property
    def is_running(self) -> bool:
        """Запущен ли цикл подключения (:meth:`connect` или :meth:`session`)."""
        return self._running

    @property
    def current_playable(self) -> Optional[ynison_state.Playable]:
        """Текущий трек очереди из последнего состояния или :obj:`None`."""
        return utils.get_current_playable(self._latest_state) if self._latest_state else None

    @property
    def active_device(self) -> Optional[ynison_state.Device]:
        """Активное устройство из последнего состояния или :obj:`None`."""
        return utils.get_active_device(self._latest_state) if self._latest_state else None

    def on_state(self, listener: ListenerT) -> ListenerT:
        """Регистрирует listener, вызываемый на каждый фрейм состояния.

        Можно использовать как декоратор. Исключения listener'а логируются
        в логгер `yandex_music.ynison` и не прерывают приём фреймов.

        Args:
            listener: Callable, принимающий
                :class:`yandex_music.ynison.models.ynison_state.PutYnisonStateResponse`.

        Returns:
            Тот же listener (для удобства использования как декоратор).
        """
        self._state_listeners.append(listener)
        return listener

    def on_error(self, listener: ErrorListener) -> ErrorListener:
        """Регистрирует listener нетерминальных ошибок.

        Вызывается на ошибки, после которых клиент продолжает работу: отклонённый
        сервером запрос (:class:`yandex_music.exceptions.YnisonServerError`) и потерю
        соединения перед переподключением (:class:`yandex_music.exceptions.YnisonConnectionClosedError`).
        Терминальные ошибки выбрасываются из :meth:`connect`.

        Args:
            listener: Callable, принимающий :class:`yandex_music.exceptions.YnisonError`.

        Returns:
            Тот же listener (для удобства использования как декоратор).
        """
        self._error_listeners.append(listener)
        return listener

    def remove_listener(self, listener: Callable[..., Any]) -> None:
        """Удаляет listener, зарегистрированный через :meth:`on_state` или :meth:`on_error`.

        Если listener не зарегистрирован, вызов игнорируется.
        """
        self._state_listeners = [item for item in self._state_listeners if item != listener]
        self._error_listeners = [item for item in self._error_listeners if item != listener]

    def _get_device_info(self, redirect: Optional[RedirectResponse]) -> str:
        device_info = {
            'Ynison-Device-Id': self._device_id,
            # да, они реально тут хотят вложенный json.dumps иначе не работает
            'Ynison-Device-Info': json_compat.dumps({'app_name': self._device_title, 'type': '1'}),  # 1: браузеры
        }
        if redirect is not None:
            device_info['Ynison-Redirect-Ticket'] = redirect.redirect_ticket
            device_info['Ynison-Session-Id'] = str(redirect.session_id)
        return json_compat.dumps(device_info)

    def _get_subprotocols(self, redirect: Optional[RedirectResponse] = None) -> List[str]:
        return ['Bearer', 'v2', urllib.parse.quote(self._get_device_info(redirect))]

    def _get_headers(self) -> Dict[str, str]:
        return {
            'Origin': 'https://music.yandex.ru',  # важно
            'Authorization': f'OAuth {self._token}',  # ещё важнее
        }

    def _redirect_uri(self) -> str:
        return f'{self._BASE_URL}/{self._REDIRECT_SERVICE}'

    def _state_uri(self, redirect: RedirectResponse) -> str:
        return f'wss://{redirect.host}/{self._STATE_SERVICE}'

    def _ping_params(self, redirect: RedirectResponse) -> Tuple[float, float]:
        params = redirect.keep_alive_params
        interval = float(params.keep_alive_time_seconds) if params else 0.0
        timeout = float(params.keep_alive_timeout_seconds) if params else 0.0
        return interval or _DEFAULT_PING_INTERVAL, timeout or _DEFAULT_PING_TIMEOUT

    def _full_state_request(self) -> ynison_state.PutYnisonStateRequest:
        return messages.build_full_state_request(self._device_id, title=self._device_title)

    @staticmethod
    def _load_frame(message: str) -> Dict[str, Any]:
        try:
            data = json_compat.loads(message)
        except ValueError as e:
            raise YnisonError(f'Некорректный фрейм от сервера: {message[:200]!r}') from e
        if not isinstance(data, dict):
            raise YnisonError(f'Некорректный фрейм от сервера: {message[:200]!r}')
        if isinstance(data.get('error'), dict):
            raise parse_server_error(data['error'])
        return data

    def _parse_redirect_frame(self, message: str) -> RedirectResponse:
        data = self._load_frame(message)
        response = RedirectResponse().from_dict(data)
        if not (response.redirect_ticket and response.session_id and response.host):
            raise YnisonError(f'Неполный ответ сервиса редиректа: {message[:200]!r}')
        self._redirect_response = response
        return response

    def _parse_state_frame(self, message: str) -> ynison_state.PutYnisonStateResponse:
        data = self._load_frame(message)
        response = ynison_state.PutYnisonStateResponse().from_dict(data)
        self._latest_state = response
        self._reconnect_attempt = 0
        return response

    def _remember_error(self, error: YnisonError) -> None:
        self._last_error = error
        if isinstance(error, YnisonServerError) and error.backoff_ms:
            self._backoff_ms = error.backoff_ms

    def _to_reconnectable_error(self, exc: BaseException) -> YnisonError:
        """Классифицирует исключение receive-loop'а.

        Returns:
            :class:`yandex_music.exceptions.YnisonError`: Ошибка, после которой нужно переподключиться.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Если ошибка терминальная.
        """
        if isinstance(exc, YnisonError):
            if is_terminal_error(exc):
                self._last_error = exc
                raise exc
            return exc
        if _transport.is_auth_failure(exc):
            self._last_error = YnisonUnauthorizedError('Сервер Ynison отклонил токен', http_code=401)
            raise self._last_error from exc

        error = YnisonConnectionClosedError(f'Соединение с Ynison потеряно: {exc!r}')
        error.__cause__ = exc
        return error

    def _next_reconnect_delay(self) -> float:
        """Увеличивает счётчик попыток и возвращает задержку перед следующей, в секундах.

        Raises:
            :class:`yandex_music.exceptions.YnisonError`: Последняя ошибка, если превышен лимит попыток.
        """
        self._reconnect_attempt += 1
        if self._max_reconnect_attempts is not None and self._reconnect_attempt > self._max_reconnect_attempts:
            error = self._last_error or YnisonError('Не удалось переподключиться к Ynison')
            raise error

        schedule = self._backoff_ms or _DEFAULT_BACKOFF_MS
        base_ms = schedule[min(self._reconnect_attempt - 1, len(schedule) - 1)]
        jitter_ms = random.uniform(0, 250)  # noqa: S311
        return (base_ms + jitter_ms) / 1000

    def _reset_connection_state(self) -> None:
        self._redirect_response = None
        self._latest_state = None
        self._last_error = None
        self._reconnect_attempt = 0
        self._backoff_ms = list(_DEFAULT_BACKOFF_MS)

    def _no_connection_error(self) -> YnisonConnectionClosedError:
        error = YnisonConnectionClosedError('Нет активного соединения с Ynison; вызовите connect() или session()')
        if self._last_error is not None and is_terminal_error(self._last_error):
            error = YnisonConnectionClosedError(f'Соединение с Ynison завершено: {self._last_error}')
            error.__cause__ = self._last_error
        return error

    def _build_set_paused_request(self, paused: bool) -> ynison_state.PutYnisonStateRequest:
        state = self.state
        if utils.get_active_device(state) is None:
            raise YnisonNoActiveDeviceError('Нет активного устройства, на котором можно поставить паузу/продолжить')
        return messages.build_set_paused_request(self._device_id, state.player_state.status, paused=paused)

    def _build_change_track_request(self, delta: int) -> ynison_state.PutYnisonStateRequest:
        return messages.build_change_track_request(self._device_id, self.state.player_state, delta=delta)

    def _build_set_volume_request(
        self, volume: float, target_device_id: Optional[str]
    ) -> ynison_state.PutYnisonStateRequest:
        target = target_device_id
        if target is None:
            active = utils.get_active_device(self.state)
            target = active.info.device_id if active is not None else None
        if not target or target == self._device_id:
            raise YnisonNoActiveDeviceError(
                'Нет активного устройства для изменения громкости; укажите target_device_id явно'
            )
        return messages.build_set_volume_request(self._device_id, target, volume)
