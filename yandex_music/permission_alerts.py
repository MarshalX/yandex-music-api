from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class PermissionAlerts(YandexMusicObject):
    """Класс, представляющий оповещения.

    Attributes:
        alerts (:obj:`list` из :obj:`str`): Список оповещений.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        alerts (:obj:`list` из :obj:`str`): Список оповещений.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 alerts: List[str],
                 client: Optional['Client'] = None,
                 **kwargs):
        self.alerts = alerts

        self.client = client

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
