from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.music_history.music_history_item import MusicHistoryItem


@model
class MusicHistoryItems(YandexMusicModel):
    """Класс, представляющий результат запроса элементов истории прослушивания.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.MusicHistoryItem`, optional): Список элементов истории.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: Optional[List['MusicHistoryItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MusicHistoryItems']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MusicHistoryItems`: Результат запроса элементов истории прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.music_history.music_history_item import MusicHistoryItem

        cls_data['items'] = MusicHistoryItem.de_list(cls_data.get('items'), client)

        return cls(client=client, **cls_data)
