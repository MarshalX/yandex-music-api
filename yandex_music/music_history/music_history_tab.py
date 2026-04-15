from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.music_history.music_history_group import MusicHistoryGroup


@model
class MusicHistoryTab(YandexMusicModel):
    """Класс, представляющий вкладку (день) истории прослушивания.

    Attributes:
        date (:obj:`str`, optional): Дата в формате ``YYYY-MM-DD``.
        items (:obj:`list` из :obj:`yandex_music.MusicHistoryGroup`, optional): Список групп прослушивания за день.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    date: Optional[str] = None
    items: Optional[List['MusicHistoryGroup']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.date,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MusicHistoryTab']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MusicHistoryTab`: Вкладка истории прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.music_history.music_history_group import MusicHistoryGroup

        cls_data['items'] = MusicHistoryGroup.de_list(cls_data.get('items'), client)

        return cls(client=client, **cls_data)
