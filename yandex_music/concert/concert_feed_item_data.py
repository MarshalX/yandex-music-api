from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert import Concert
    from yandex_music.concert.concert_min_price import ConcertMinPrice


@model
class ConcertFeedItemData(YandexMusicModel):
    """Класс, представляющий данные элемента ленты концертов.

    Attributes:
        concert (:obj:`yandex_music.Concert`, optional): Концерт.
        min_price (:obj:`yandex_music.ConcertMinPrice`, optional): Минимальная цена билета.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    concert: Optional['Concert'] = None
    min_price: Optional['ConcertMinPrice'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.concert,)
