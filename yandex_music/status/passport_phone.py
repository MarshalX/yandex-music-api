from yandex_music import YandexMusicObject


class PassportPhone(YandexMusicObject):
    """Класс представляющий номер телефона пользователя.

    Attributes:
        phone (:obj:`str`): Номер телефона.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        phone (:obj:`str`): Номер телефона.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 phone,
                 client=None,
                 **kwargs):
        self.phone = phone

        self.client = client
        self._id_attrs = (self.phone,)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.PassportPhone`: Объект класса :class:`yandex_music.PassportPhone`.
        """
        if not data:
            return None

        data = super(PassportPhone, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.PassportPhone`: Список объектов класса :class:`yandex_music.PassportPhone`.
        """
        if not data:
            return []

        phones = list()
        for phone in data:
            phones.append(cls.de_json(phone, client))

        return phones
