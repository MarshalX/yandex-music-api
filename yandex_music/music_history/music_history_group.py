from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.music_history.music_history_item import MusicHistoryItem


@model
class MusicHistoryGroup(YandexMusicModel):
    """Класс, представляющий группу элементов истории прослушивания.

    Note:
        Группа содержит контекст (например, альбом) и список прослушанных треков
        в рамках этого контекста.

    Attributes:
        context (:obj:`yandex_music.MusicHistoryItem`, optional): Контекст прослушивания (альбом, плейлист и т.д.).
        tracks (:obj:`list` из :obj:`yandex_music.MusicHistoryItem`, optional): Список прослушанных треков.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    context: Optional['MusicHistoryItem'] = None
    tracks: Optional[List['MusicHistoryItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.context,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MusicHistoryGroup']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MusicHistoryGroup`: Группа элементов истории прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.music_history.music_history_item import MusicHistoryItem

        cls_data['context'] = MusicHistoryItem.de_json(cls_data.get('context'), client)
        cls_data['tracks'] = MusicHistoryItem.de_list(cls_data.get('tracks'), client)

        return cls(client=client, **cls_data)
