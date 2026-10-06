from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert_feed_item_data import ConcertFeedItemData


@model
class ConcertFeedItem(YandexMusicModel):
    """Класс, представляющий элемент ленты концертов.

    Note:
        Известные значения поля ``type``: ``concert_item``.

    Attributes:
        type (:obj:`str`, optional): Тип элемента ленты.
        data (:obj:`yandex_music.ConcertFeedItemData`, optional): Данные элемента ленты.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional['ConcertFeedItemData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)
