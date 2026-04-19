"""Билдеры запросов Ynison.

Набор функций для конструирования :class:`PutYnisonStateRequest` под типичные
действия: инициализация подключения, пауза/возобновление, переключение трека,
изменение громкости. Используется как долгоживущими клиентами
(:class:`yandex_music.ynison.YnisonClient`, :class:`yandex_music.ynison.YnisonClientAsync`),
так и простыми интерфейсами из :mod:`yandex_music.ynison.simple` /
:mod:`yandex_music.ynison.simple_async`.
"""

import dataclasses
import time
from random import random
from typing import Any
from uuid import uuid4

from yandex_music.ynison.models import ynison_state


def generate_device_id() -> str:
    """Генерирует случайный идентификатор устройства.

    Returns:
        :obj:`str`: Идентификатор в hex-представлении (без префикса `0x`).
    """
    return hex(int(10**16 * random()))[2:]  # noqa: S311


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


def get_update_full_state_request(device_id: str) -> ynison_state.PutYnisonStateRequest:
    """Собирает начальный запрос регистрации устройства как remote control.

    Отправляется сразу после подключения state websocket'а. Регистрирует
    устройство с возможностями дистанционного пульта (не плеер) и пустой
    очередью воспроизведения.

    Args:
        device_id: Идентификатор этого устройства.

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
                    title='Python SDK',
                    app_name='yandex-music',
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


def get_update_player_state_request(device_id: str) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос с пустым состоянием плеера.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` с пустой очередью.
    """
    return ynison_state.PutYnisonStateRequest(
        update_player_state=ynison_state.UpdatePlayerState(
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
        ),
        rid=generate_request_id(),
        player_action_timestamp_ms=get_timestamp(),
        activity_interception_type=ynison_state.PutYnisonStateRequestActivityInterceptionType.DO_NOT_INTERCEPT_BY_DEFAULT,
    )


def get_set_paused_request(
    device_id: str,
    current_status: ynison_state.PlayingStatus,
    paused: bool,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос паузы или возобновления воспроизведения.

    Клонирует текущий `PlayingStatus`, меняя только флаг `paused` и обновляя версию.
    Прочие поля (`progress_ms`, `duration_ms`, `playback_speed`) сохраняются.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_status: Текущий статус воспроизведения с сервера.
        paused: `True` — поставить на паузу, `False` — продолжить.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayingStatus` с подменённым флагом `paused`.
    """
    new_status = ynison_state.PlayingStatus(
        progress_ms=current_status.progress_ms,
        duration_ms=current_status.duration_ms,
        paused=paused,
        playback_speed=current_status.playback_speed or 1.0,
        version=_new_version(device_id),
    )
    return _wrap_request(
        update_playing_status=ynison_state.UpdatePlayingStatus(playing_status=new_status),
    )


def get_change_track_request(
    device_id: str,
    current_state: ynison_state.PlayerState,
    delta: int,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос перехода на соседний трек в очереди.

    Клонирует текущий :class:`PlayerQueue`, меняя только `current_playable_index`
    и версию. Статус воспроизведения сбрасывается на нулевой прогресс
    с сохранением флага паузы.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_state: Текущее состояние плеера с сервера.
        delta: Сдвиг индекса; `1` — следующий трек, `-1` — предыдущий.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` с обновлённым индексом и версией.
    """
    queue = current_state.player_queue
    total = len(queue.playable_list)
    new_index = max(0, min(queue.current_playable_index + delta, total - 1)) if total else -1

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


def get_next_track_request(
    device_id: str,
    current_state: ynison_state.PlayerState,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос перехода на следующий трек.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_state: Текущее состояние плеера с сервера.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` с индексом, увеличенным на 1.
    """
    return get_change_track_request(device_id, current_state, delta=1)


def get_prev_track_request(
    device_id: str,
    current_state: ynison_state.PlayerState,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос перехода на предыдущий трек.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        current_state: Текущее состояние плеера с сервера.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.PutYnisonStateRequest`:
            Запрос `UpdatePlayerState` с индексом, уменьшенным на 1.
    """
    return get_change_track_request(device_id, current_state, delta=-1)


def get_set_volume_request(
    device_id: str,
    target_device_id: str,
    volume: float,
) -> ynison_state.PutYnisonStateRequest:
    """Собирает запрос изменения громкости на целевом устройстве.

    Args:
        device_id: Идентификатор устройства, инициировавшего изменение.
        target_device_id: Идентификатор устройства, на котором меняется громкость.
        volume: Новая громкость в диапазоне [0.0; 1.0]; вне диапазона — клампится.

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
