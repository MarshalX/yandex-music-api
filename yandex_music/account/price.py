from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Price(YandexMusicModel):
    """Класс, представляющий цену.

    Attributes:
        amount (:obj:`int`): Количество единиц.
        currency (:obj:`str`): Валюта.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    amount: int
    currency: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.amount, self.currency)
