from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.music_history.music_history_item_data import MusicHistoryItemData


@model
class MusicHistoryItem(YandexMusicModel):
    """Класс, представляющий элемент истории прослушивания.

    Note:
        Известные значения поля `type`: ``track``, ``album``.

    Attributes:
        type (:obj:`str`): Тип элемента.
        data (:obj:`yandex_music.MusicHistoryItemData`, optional): Данные элемента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    data: Optional['MusicHistoryItemData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MusicHistoryItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MusicHistoryItem`: Элемент истории прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.music_history.music_history_item_data import MusicHistoryItemData

        item_type = cls_data.get('type')
        cls_data['data'] = MusicHistoryItemData.de_json(cls_data.get('data'), client, item_type=item_type)

        return cls(client=client, **cls_data)
