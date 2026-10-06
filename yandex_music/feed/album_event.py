from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Album, ClientType, Track


@model
class AlbumEvent(YandexMusicModel):
    """Класс, представляющий альбом в событии фида.

    Attributes:
        album (:obj:`yandex_music.Album`, optional): Альбом.
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional['Album']
    tracks: List['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.album, self.tracks)
