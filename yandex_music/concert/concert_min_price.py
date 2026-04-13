from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ConcertMinPrice(YandexMusicModel):
    """Класс, представляющий минимальную цену билета на концерт.

    Attributes:
        value (:obj:`int`, optional): Значение цены.
        currency (:obj:`str`, optional): Код валюты, например "RUB".
        currency_symbol (:obj:`str`, optional): Символ валюты, например "₽".
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    value: Optional[int] = None
    currency: Optional[str] = None
    currency_symbol: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.value, self.currency)
