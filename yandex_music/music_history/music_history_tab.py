from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
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
