from yandex_music import YandexMusicObject


class Price(YandexMusicObject):
    """Класс представляющий цену.

    Attributes:
        amount (:obj:`int`): Количество единиц.
        currency (:obj:`str`): Валюта.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        amount (:obj:`int`): Количество единиц.
        currency (:obj:`str`): Валюта.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 amount,
                 currency,
                 client=None,
                 **kwargs):
        self.amount = amount
        self.currency = currency

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Price`: Объект класса :class:`yandex_music.Price`.
        """
        if not data:
            return None

        data = super(Price, cls).de_json(data, client)

        return cls(client=client, **data)
