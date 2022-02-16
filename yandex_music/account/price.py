from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Price(YandexMusicObject):
    """Класс, представляющий цену.

    Attributes:
        amount (:obj:`int`): Количество единиц.
        currency (:obj:`str`): Валюта.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    amount: int
    currency: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.amount, self.currency)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Price']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Price`: Цена.
        """
        if not data:
            return None

        data = super(Price, cls).de_json(data, client)

        return cls(client=client, **data)
