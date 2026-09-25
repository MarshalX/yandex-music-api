"""Билдеры запросов Ynison.

Набор функций для конструирования :class:`PutYnisonStateRequest` под типичные
действия: инициализация подключения, пауза/возобновление, переключение трека,
изменение громкости. Используется клиентами
(:class:`yandex_music.ynison.YnisonClient`, :class:`yandex_music.ynison.YnisonClientAsync`)
в их методах управления (``pause``, ``next_track`` и т.д.). Вызывать билдеры напрямую
нужно только для собственных сценариев через ``client.send(request)``.
"""

import dataclasses
import hashlib
import time
from random import random
from typing import Any, Optional
from uuid import uuid4

from yandex_music.exceptions import YnisonQueueBoundaryError
from yandex_music.ynison import utils
from yandex_music.ynison.models import ynison_state

DEFAULT_DEVICE_TITLE = 'Python SDK'
DEFAULT_APP_NAME = 'yandex-music'


def generate_device_id(seed: Optional[str] = None) -> str:
    """Генерирует идентификатор устройства.

    Без `seed` случайный. С `seed` детерминированный: один и тот же `seed`
    всегда даёт один и тот же идентификатор, поэтому повторные запуски не плодят
    новые устройства в Ynison-сессии.

    Args:
        seed: Произвольная строка для детерминированной генерации.

    Returns:
        :obj:`str`: Идентификатор из 12 hex-символов.
    """
    if seed is None:
        return f'{int(2**48 * random()):012x}'  # noqa: S311
    return hashlib.sha256(seed.encode('UTF-8')).hexdigest()[:12]


def get_timestamp() -> int:
    """Возвращает текущее unix-время в миллисекундах.

    Returns:
        :obj:`int`: Время в миллисекундах от эпохи Unix.
    """
    return int(time.time() * 1000)


def generate_request_id() -> str:
    """Генерирует уникальный идентификатор запроса.

    Returns:
        :obj:`str`: UUID4 в строковом представлении.
    """
    return str(uuid4())


def _new_version(device_id: str) -> ynison_state.UpdateVersion:
    return ynison_state.UpdateVersion(
        device_id=device_id,
        version=int(10**18 * random()),  # noqa: S311
        timestamp_ms=get_timestamp(),
    )


def _wrap_request(**oneof: Any) -> ynison_state.PutYnisonStateRequest:
    return ynison_state.PutYnisonStateRequest(
        rid=generate_request_id(),
        player_action_timestamp_ms=get_timestamp(),
        activity_interception_type=ynison_state.PutYnisonStateRequestActivityInterceptionType.DO_NOT_INTERCEPT_BY_DEFAULT,
        **oneof,
    )


def build_full_state_request(
    device_id: str,
    title: str = DEFAULT_DEVICE_TITLE,
    app_name: str = DEFAULT_APP_NAME,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает начальный запрос регистрации устройства как remote control.

    Отправляется сразу после подключения state websocket'а. Регистрирует
    устройство с возможностями дистанционного пульта (не плеер) и пустой
    очередью воспроизведения.

    Args:
        device_id: Идентификатор этого устройства.
        title: Название устройства, которое увидят другие клиенты в списке устройств.
        app_name: Название приложения.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdateFullState` с device capabilities remote control.
    """
    return ynison_state.PutYnisonStateRequest(
        update_full_state=ynison_state.UpdateFullState(
            player_state=ynison_state.PlayerState(
                player_queue=ynison_state.PlayerQueue(
                    current_playable_index=-1,
                    options=ynison_state.PlayerStateOptions(
                        repeat_mode=ynison_state.PlayerStateOptionsRepeatMode.NONE,
                    ),
                    version=ynison_state.UpdateVersion(
                        device_id=device_id,
                    ),
                    entity_id='',
                    entity_type=ynison_state.PlayerQueueEntityType.VARIOUS,
                    entity_context=ynison_state.PlayerQueueEntityContext.BASED_ON_ENTITY_BY_DEFAULT,
                    from_optional='',
                ),
                status=ynison_state.PlayingStatus(
                    paused=True,
                    playback_speed=1,
                    version=ynison_state.UpdateVersion(
                        device_id=device_id,
                        timestamp_ms=0,
                    ),
                ),
            ),
            device=ynison_state.UpdateDevice(
                capabilities=ynison_state.DeviceCapabilities(
                    can_be_player=False,
                    can_be_remote_controller=True,
                    volume_granularity=0,
                ),
                info=ynison_state.DeviceInfo(
                    device_id=device_id,
                    type=ynison_state.DeviceType.WEB,
                    title=title,
                    app_name=app_name,
                ),
                volume_info=ynison_state.DeviceVolume(
                    volume=0,
                ),
            ),
            is_currently_active=False,
        ),
        rid=generate_request_id(),
        player_action_timestamp_ms=0,
        activity_interception_type=ynison_state.PutYnisonStateRequestActivityInterceptionType.DO_NOT_INTERCEPT_BY_DEFAULT,
    )


def build_set_paused_request(
    device_id: str,
    current_status: ynison_state.PlayingStatus,
    paused: bool,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос паузы или возобновления воспроизведения.

    Клонирует текущий `PlayingStatus`, меняя флаг `paused` и обновляя версию.
    Прогресс пересчитывается на текущий момент (см. :func:`yandex_music.ynison.utils.get_current_progress_ms`),
    иначе пауза откатила бы трек к позиции из последнего фрейма.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_status: Текущий статус воспроизведения с сервера.
        paused: `True`, чтобы поставить на паузу, `False`, чтобы продолжить.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayingStatus` с подменённым флагом `paused`.
    """
    new_status = ynison_state.PlayingStatus(
        progress_ms=utils.get_current_progress_ms(current_status),
        duration_ms=current_status.duration_ms,
        paused=paused,
        playback_speed=current_status.playback_speed or 1.0,
        version=_new_version(device_id),
    )
    return _wrap_request(
        update_playing_status=ynison_state.UpdatePlayingStatus(playing_status=new_status),
    )


def build_change_track_request(
    device_id: str,
    current_state: ynison_state.PlayerState,
    delta: int,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос перехода на соседний трек в очереди.

    Клонирует текущий :class:`PlayerQueue`, меняя только `current_playable_index`
    и версию. Сдвиг считается в порядке воспроизведения, то есть с учётом
    перемешивания. Статус воспроизведения сбрасывается на нулевой прогресс
    с сохранением флага паузы; длительность нового трека в очереди неизвестна
    и выставляется в `0`, её заполнит устройство-плеер.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_state: Текущее состояние плеера с сервера.
        delta: Сдвиг в порядке воспроизведения; `1` для следующего трека, `-1` для предыдущего.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` с обновлённым индексом и версией.

    Raises:
        :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если сдвиг выходит
            за пределы очереди (например, `next` на последнем треке).
    """
    queue = current_state.player_queue
    new_index = utils.get_neighbour_index(queue, delta)
    if new_index is None:
        raise YnisonQueueBoundaryError(
            f'Нельзя сдвинуться на {delta:+d} от трека {queue.current_playable_index} '
            f'в очереди из {len(queue.playable_list)} треков'
        )

    new_queue = dataclasses.replace(
        queue,
        current_playable_index=new_index,
        version=_new_version(device_id),
    )
    new_status = ynison_state.PlayingStatus(
        progress_ms=0,
        duration_ms=0,
        paused=current_state.status.paused,
        playback_speed=current_state.status.playback_speed or 1.0,
        version=_new_version(device_id),
    )
    return _wrap_request(
        update_player_state=ynison_state.UpdatePlayerState(
            player_state=ynison_state.PlayerState(player_queue=new_queue, status=new_status),
        ),
    )


def build_next_track_request(
    device_id: str,
    current_state: ynison_state.PlayerState,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос перехода на следующий трек.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_state: Текущее состояние плеера с сервера.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` со следующим индексом.

    Raises:
        :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек последний.
    """
    return build_change_track_request(device_id, current_state, delta=1)


def build_previous_track_request(
    device_id: str,
    current_state: ynison_state.PlayerState,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос перехода на предыдущий трек.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_state: Текущее состояние плеера с сервера.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` с предыдущим индексом.

    Raises:
        :class:`yandex_music.exceptions.YnisonQueueBoundaryError`: Если текущий трек первый.
    """
    return build_change_track_request(device_id, current_state, delta=-1)


def build_set_volume_request(
    device_id: str,
    target_device_id: str,
    volume: float,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос изменения громкости на целевом устройстве.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        target_device_id: Идентификатор устройства, на котором меняется громкость.
        volume: Новая громкость в диапазоне [0.0; 1.0]; значения вне диапазона обрезаются.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdateVolumeInfo` с новым значением громкости и версией.
    """
    volume = max(0.0, min(1.0, volume))
    return _wrap_request(
        update_volume_info=ynison_state.UpdateVolumeInfo(
            device_id=target_device_id,
            volume_info=ynison_state.DeviceVolume(
                volume=volume,
                version=_new_version(device_id),
            ),
        ),
    )
