from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.playlist.playlist import Playlist


@model
class PlaylistsList(YandexMusicModel):
    """Класс, представляющий список плейлистов.

    Attributes:
        playlists (:obj:`list` из :obj:`yandex_music.Playlist`, optional): Список плейлистов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    playlists: Optional[List['Playlist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.playlists,)
