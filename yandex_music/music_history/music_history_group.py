from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
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
