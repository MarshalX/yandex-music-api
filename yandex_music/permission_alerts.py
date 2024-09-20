from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PermissionAlerts(YandexMusicModel):
    """Класс, представляющий оповещения.

    Attributes:
        alerts (:obj:`list` из :obj:`str`): Список оповещений.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    alerts: List[str]
    client: Optional['Client'] = None
