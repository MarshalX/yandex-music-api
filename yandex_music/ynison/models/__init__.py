"""Модели Ynison.

Модели сгенерированы из protobuf-схем Ynison (см. :mod:`yandex_music.ynison.models.ynison_state`).
Для удобства ключевые модели доступны прямо из этого пакета, а ответ сервера
с полным состоянием доступен под коротким именем :obj:`YnisonState`.
"""

from yandex_music.ynison.models import ynison_redirect, ynison_state
from yandex_music.ynison.models.ynison_state import (
    Device,
    DeviceInfo,
    DeviceVolume,
    Playable,
    PlayerQueue,
    PlayerState,
    PlayingStatus,
    PutYnisonStateRequest,
    PutYnisonStateResponse,
)

YnisonState = PutYnisonStateResponse
"""Полное состояние Ynison: плеер, очередь и устройства. Псевдоним :class:`PutYnisonStateResponse`."""

__all__ = [
    'Device',
    'DeviceInfo',
    'DeviceVolume',
    'Playable',
    'PlayerQueue',
    'PlayerState',
    'PlayingStatus',
    'PutYnisonStateRequest',
    'PutYnisonStateResponse',
    'YnisonState',
    'ynison_redirect',
    'ynison_state',
]
