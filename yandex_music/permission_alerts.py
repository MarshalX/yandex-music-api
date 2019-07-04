from yandex_music import YandexMusicObject


class PermissionAlerts(YandexMusicObject):
    """Класс представляющий оповещения.

    Attributes:
        alerts (:obj:`list` из :obj:`str`): Список оповещений.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        alerts (:obj:`list` из :obj:`str`): Список оповещений.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 alerts,
                 client=None,
                 **kwargs):
        self.alerts = alerts

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.PermissionAlerts`: Объект класса :class:`yandex_music.PermissionAlerts`.
        """
        if not data:
            return None

        data = super(PermissionAlerts, cls).de_json(data, client)

        return cls(client=client, **data)
