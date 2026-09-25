"""Простой асинхронный интерфейс Ynison.

Каждая корутина открывает свежее websocket-соединение, выполняет одно действие
и корректно закрывается. Для долгоживущих подключений или собственных payload'ов
используйте :class:`yandex_music.ynison.YnisonClientAsync` напрямую.

Note:
    По умолчанию все функции используют один детерминированный `device_id`,
    вычисленный из токена. Параллельные вызовы с одним `device_id` вытесняют
    друг друга (:class:`yandex_music.exceptions.YnisonDeviceDisplacedError`).

Синхронный аналог :mod:`yandex_music.ynison.simple`.
"""

from typing import List, Optional

from yandex_music.ynison import messages, utils
from yandex_music.ynison.client_async import YnisonClientAsync
from yandex_music.ynison.models import ynison_state

_DEFAULT_TIMEOUT = 10.0


def _client(token: str, device_id: Optional[str]) -> YnisonClientAsync:
    # свой device_id, чтобы не вытеснять долгоживущий клиент с дефолтным id
    default_device_id = messages.generate_device_id(seed=f'yandex-music-ynison-simple:{token}')
    return YnisonClientAsync(token, device_id or default_device_id)


async def get_state(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> ynison_state.PutYnisonStateResponse:
    """Возвращает текущее состояние плеера со всеми устройствами.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateResponse`:
            Последний полученный фрейм состояния.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        return client.state


async def get_current_track(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> Optional[ynison_state.Playable]:
    """Возвращает текущий трек в очереди активного устройства.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.Playable` | :obj:`None`:
            Текущий playable или :obj:`None`, если индекс вне списка
            (пустая очередь или незавершённый старт).

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        return utils.get_current_playable(client.state)


async def get_devices(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> List[ynison_state.Device]:
    """Возвращает список всех устройств в текущей Ynison-сессии.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`list` из :obj:`yandex_music.ynison.models.ynison_state.Device`:
            Все известные устройства, включая оффлайн.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        return list(client.state.devices)


async def get_active_device(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> Optional[ynison_state.Device]:
    """Возвращает активное (играющее) устройство.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.Device` | :obj:`None`:
            Активное устройство или :obj:`None`, если ни одно устройство
            не играет прямо сейчас.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        return utils.get_active_device(client.state)


async def pause(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Ставит воспроизведение на паузу на активном устройстве.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
        :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если нет активного устройства.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        await client.pause()


async def resume(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Снимает паузу на активном устройстве.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
        :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если нет активного устройства.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        await client.resume()


async def next_track(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Переключает на следующий трек в очереди.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
        :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек последний.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        await client.next_track()


async def previous_track(
    token: str,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Переключает на предыдущий трек в очереди.

    Args:
        token: OAuth-токен Yandex Music.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
        :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек первый.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        await client.previous_track()


async def set_volume(
    token: str,
    volume: float,
    target_device_id: Optional[str] = None,
    device_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> None:
    """Устанавливает громкость на указанном или активном устройстве.

    Args:
        token: OAuth-токен Yandex Music.
        volume: Громкость в диапазоне [0.0; 1.0]; значения вне диапазона обрезаются.
        target_device_id: Идентификатор устройства, на котором меняется громкость.
            Если :obj:`None`, берётся активное устройство из текущего состояния.
        device_id: Идентификатор этого клиента в Ynison-сессии.
            По умолчанию детерминированный, вычисленный из токена.
        timeout: Максимальное время ожидания начального фрейма, в секундах.

    Raises:
        :class:`yandex_music.exceptions.YnisonNoActiveDeviceError`: Если не удалось определить
            целевое устройство (нет активного и не передан `target_device_id`).
        :class:`yandex_music.exceptions.YnisonTimeoutError`: Если начальный фрейм не пришёл за `timeout` секунд.
        :class:`yandex_music.exceptions.YnisonUnauthorizedError`: Неверный или истёкший токен.
    """
    async with _client(token, device_id).session(timeout=timeout) as client:
        await client.set_volume(volume, target_device_id)
