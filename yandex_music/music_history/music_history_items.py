from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
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
