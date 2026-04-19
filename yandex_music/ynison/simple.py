##############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/ynison/simple_async.py. DON'T EDIT IT BY HANDS #
##############################################################################################

"""Простой интерфейс Ynison.

Каждая функция открывает свежее websocket-соединение, выполняет одно действие
и корректно закрывается. Для долгоживущих подключений или собственных payload'ов
используйте :class:`yandex_music.ynison.YnisonClient` напрямую вместе с билдерами
запросов из :mod:`yandex_music.ynison.messages`.

Синхронный аналог :mod:`yandex_music.ynison.simple`.
"""

from typing import List, Optional

from yandex_music.exceptions import YnisonError
from yandex_music.ynison import messages
from yandex_music.ynison._client import YnisonClient
from yandex_music.ynison.models import ynison_state

_DEFAULT_TIMEOUT = 10.0


def get_state(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> ynison_state.PutYnisonStateResponse:
    """Возвращает текущее состояние плеера со всеми устройствами.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateResponse`:
            Последний полученный фрейм состояния.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        return client._require_state()


def get_current_track(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> Optional[ynison_state.Playable]:
    """Возвращает текущий трек в очереди активного устройства.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.Playable` | :obj:`None`:
            Текущий playable или :obj:`None`, если индекс вне списка
            (пустая очередь или незавершённый старт).

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        queue = client._require_state().player_state.player_queue
        idx = queue.current_playable_index
        if 0 <= idx < len(queue.playable_list):
            return queue.playable_list[idx]
        return None


def get_devices(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> List[ynison_state.Device]:
    """Возвращает список всех устройств в текущей Ynison-сессии.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`list` из :obj:`yandex_music.ynison.models.ynison_state.Device`:
            Все известные устройства, включая оффлайн.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        return list(client._require_state().devices)


def get_active_device(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> Optional[ynison_state.Device]:
    """Возвращает активное (играющее) устройство.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.Device` | :obj:`None`:
            Активное устройство или :obj:`None`, если ни одно устройство
            не играет прямо сейчас.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        state = client._require_state()
        active_id = state.active_device_id_optional
        if not active_id:
            return None
        return next((d for d in state.devices if d.info.device_id == active_id), None)


def pause(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Ставит воспроизведение на паузу на активном устройстве.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        status = client._require_state().player_state.status
        client.send(messages.get_set_paused_request(client.device_id, status, paused=True))


def resume(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Снимает паузу на активном устройстве.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        status = client._require_state().player_state.status
        client.send(messages.get_set_paused_request(client.device_id, status, paused=False))


def next_track(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Переключает на следующий трек в очереди.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        state = client._require_state().player_state
        client.send(messages.get_next_track_request(client.device_id, state))


def previous_track(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Переключает на предыдущий трек в очереди.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        state = client._require_state().player_state
        client.send(messages.get_prev_track_request(client.device_id, state))


def set_volume(
    token: str,
    volume: float,
    target_device_id: Optional[str] = None,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Устанавливает громкость на указанном или активном устройстве.

    Args:
        token: OAuth-токен Yandex Music.
        volume: Громкость в диапазоне [0.0; 1.0]; вне диапазона — клампится билдером.
        target_device_id: Идентификатор устройства, на котором меняется громкость.
            Если :obj:`None` — берётся активное устройство из текущего состояния.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию — случайный.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonError`: Если не удалось определить
            целевое устройство (нет активного и не передан `target_device_id`)
            или начальный фрейм не пришёл за `timeout` секунд.
    """
    with YnisonClient(token, device_id).session(timeout=timeout) as client:
        state = client._require_state()
        target = target_device_id or state.active_device_id_optional
        if not target or target == client.device_id:
            raise YnisonError('Нет активного устройства для изменения громкости; укажите target_device_id явно')
        client.send(messages.get_set_volume_request(client.device_id, target, volume))
