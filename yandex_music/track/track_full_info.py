from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType
    from yandex_music.track.track import Track


@model
class TrackFullInfo(YandexMusicModel):
    """Класс, представляющий полную информацию о треке.

    Attributes:
        track (:obj:`yandex_music.Track`, optional): Трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`, optional): Список похожих треков.
        also_in_albums (:obj:`list` из :obj:`yandex_music.Track`, optional): Список треков из других альбомов.
        aliases (:obj:`list` из :obj:`str`, optional): Список псевдонимов трека.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов с подробной информацией.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track'] = None
    similar_tracks: Optional[List['Track']] = None
    also_in_albums: Optional[List['Track']] = None
    aliases: Optional[List[str]] = None
    artists: Optional[List['Artist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track,)
