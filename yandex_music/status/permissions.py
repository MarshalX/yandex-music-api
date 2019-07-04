from datetime import datetime

from yandex_music import YandexMusicObject


class Permissions(YandexMusicObject):
    """Класс предоставляющий информацию о правах пользователя, их изначальных значениях и даты окончания.

    Attributes:
        until (:obj:`datetime.datetime`): Дата окончания прав.
        values (:obj:`list` из :obj:`str`): Список прав.
        default (:obj:`list` из :obj:`str`): Список изначальных прав.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.

    Args:
        until (:obj:`str`): Дата окончания прав.
        values (:obj:`list` из :obj:`str`): Список прав.
        default (:obj:`list` из :obj:`str`): Список изначальных прав.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 until,
                 values,
                 default,
                 client=None,
                 **kwargs):
        self.until = datetime.fromisoformat(until)
        self.values = values
        self.default = default

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Permissions`: Объект класса :class:`yandex_music.Permissions`.
        """
        if not data:
            return None

        data = super(Permissions, cls).de_json(data, client)

        return cls(client=client, **data)
