from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert_feed_item import ConcertFeedItem


@model
class ConcertFeed(YandexMusicModel):
    """Класс, представляющий ленту концертов.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ConcertFeedItem`): Элементы ленты.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: List['ConcertFeedItem'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items,)
