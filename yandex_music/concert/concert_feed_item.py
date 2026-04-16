from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ConcertFeedItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ConcertFeedItem`: Элемент ленты концертов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert_feed_item_data import ConcertFeedItemData

        cls_data['data'] = ConcertFeedItemData.de_json(cls_data.get('data'), client)

        return cls(client=client, **cls_data)
