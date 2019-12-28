from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

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
                 amount: int,
                 currency: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.amount = amount
        self.currency = currency

        self.client = client
        self._id_attrs = (self.amount, self.currency)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Price']:
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
