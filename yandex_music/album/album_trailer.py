from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.album.album import Album
    from yandex_music.artist.artist import Artist
    from yandex_music.trailer_info import TrailerInfo


@model
class AlbumTrailer(YandexMusicModel):
    """Класс, представляющий трейлер альбома.

    Attributes:
        album (:obj:`yandex_music.Album`, optional): Альбом.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов.
        trailer (:obj:`yandex_music.TrailerInfo`, optional): Информация о трейлере.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional['Album'] = None
    artists: Optional[List['Artist']] = None
    trailer: Optional['TrailerInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.album, self.trailer)
