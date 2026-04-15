from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.music_history.music_history_tab import MusicHistoryTab


@model
class MusicHistory(YandexMusicModel):
    """Класс, представляющий историю прослушивания.

    Attributes:
        history_tabs (:obj:`list` из :obj:`yandex_music.MusicHistoryTab`, optional):
            Список вкладок (дней) истории прослушивания.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    history_tabs: Optional[List['MusicHistoryTab']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.history_tabs,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MusicHistory']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MusicHistory`: История прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.music_history.music_history_tab import MusicHistoryTab

        cls_data['history_tabs'] = MusicHistoryTab.de_list(cls_data.get('history_tabs'), client)

        return cls(client=client, **cls_data)
