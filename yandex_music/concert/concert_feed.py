from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ConcertFeed']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ConcertFeed`: Лента концертов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert_feed_item import ConcertFeedItem

        cls_data['items'] = ConcertFeedItem.de_list(cls_data.get('items'), client)

        return cls(client=client, **cls_data)
