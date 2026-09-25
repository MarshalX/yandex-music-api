"""Хелперы для чтения состояния Ynison.

Функции принимают модели из :mod:`yandex_music.ynison.models.ynison_state` и
инкапсулируют типовые вычисления: текущий трек, активное устройство,
порядок воспроизведения с учётом перемешивания, актуальный прогресс.
"""

import time
from typing import List, Optional

from yandex_music.ynison.models import ynison_state


def get_current_playable(state: ynison_state.PutYnisonStateResponse) -> Optional[ynison_state.Playable]:
    """Возвращает текущий трек в очереди.

    Args:
        state: Состояние Ynison.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.Playable` | :obj:`None`: Текущий playable
            или :obj:`None`, если очередь пуста или индекс вне списка.
    """
    queue = state.player_state.player_queue
    idx = queue.current_playable_index
    if 0 <= idx < len(queue.playable_list):
        return queue.playable_list[idx]
    return None


def get_active_device(state: ynison_state.PutYnisonStateResponse) -> Optional[ynison_state.Device]:
    """Возвращает активное (играющее) устройство.

    Args:
        state: Состояние Ynison.

    Returns:
        :obj:`yandex_music.ynison.models.ynison_state.Device` | :obj:`None`: Активное устройство
            или :obj:`None`, если ни одно устройство не активно.
    """
    active_id = state.active_device_id_optional
    if not active_id:
        return None
    return next((d for d in state.devices if d.info.device_id == active_id), None)


def get_playback_order(queue: ynison_state.PlayerQueue) -> List[int]:
    """Возвращает порядок воспроизведения индексов очереди.

    Если включено перемешивание, порядок берётся из :attr:`Shuffle.playable_indices`,
    иначе индексы идут по порядку.

    Args:
        queue: Очередь воспроизведения.

    Returns:
        :obj:`list` из :obj:`int`: Индексы `playable_list` в порядке воспроизведения.
    """
    total = len(queue.playable_list)
    shuffle = queue.shuffle_optional
    indices = list(shuffle.playable_indices) if shuffle is not None else []
    if indices and len(indices) == total:
        return indices
    return list(range(total))


def get_neighbour_index(queue: ynison_state.PlayerQueue, delta: int) -> Optional[int]:
    """Возвращает индекс трека, соседнего с текущим в порядке воспроизведения.

    Args:
        queue: Очередь воспроизведения.
        delta: Сдвиг в порядке воспроизведения; `1` для следующего, `-1` для предыдущего.

    Returns:
        :obj:`int` | :obj:`None`: Индекс в `playable_list` или :obj:`None`, если сдвиг
            выходит за границы очереди или текущий трек не определён.
    """
    order = get_playback_order(queue)
    try:
        position = order.index(queue.current_playable_index)
    except ValueError:
        return None

    new_position = position + delta
    if 0 <= new_position < len(order):
        return order[new_position]
    return None


def get_current_progress_ms(status: ynison_state.PlayingStatus, now_ms: Optional[int] = None) -> int:
    """Возвращает актуальный прогресс воспроизведения с учётом прошедшего времени.

    Сервер присылает прогресс на момент последнего изменения статуса. Пока трек
    играет, реальная позиция уходит вперёд на `(now - version.timestamp_ms) * playback_speed`.

    Args:
        status: Статус воспроизведения из состояния.
        now_ms: Текущее unix-время в миллисекундах; по умолчанию системное.

    Returns:
        :obj:`int`: Прогресс в миллисекундах, ограниченный длительностью трека (если она известна).
    """
    progress = status.progress_ms
    timestamp = status.version.timestamp_ms if status.version is not None else 0
    if not status.paused and timestamp > 0:
        if now_ms is None:
            now_ms = int(time.time() * 1000)
        elapsed = max(0, now_ms - timestamp)
        progress += int(elapsed * (status.playback_speed or 1.0))

    if status.duration_ms > 0:
        progress = min(progress, status.duration_ms)
    return progress
