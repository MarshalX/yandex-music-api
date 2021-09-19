from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PermissionAlerts(YandexMusicObject):
    """Класс, представляющий оповещения.

    Attributes:
        alerts (:obj:`list` из :obj:`str`): Список оповещений.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    alerts: List[str]
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PermissionAlerts']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PermissionAlerts`: Оповещение.
        """
        if not data:
            return None

        data = super(PermissionAlerts, cls).de_json(data, client)

        return cls(client=client, **data)
