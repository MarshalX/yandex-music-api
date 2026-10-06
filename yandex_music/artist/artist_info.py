from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist import Artist
    from yandex_music.artist.artist_trailer_status import ArtistTrailerStatus
    from yandex_music.artist.stats import Stats
    from yandex_music.cover import Cover


@model
class ArtistInfo(YandexMusicModel):
    """Класс, представляющий подробную информацию об артисте.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        likes_count (:obj:`int`, optional): Количество лайков.
        stats (:obj:`yandex_music.Stats`, optional): Статистика прослушиваний.
        trailer (:obj:`yandex_music.ArtistTrailerStatus`, optional): Статус доступности трейлера.
        covers (:obj:`list` из :obj:`yandex_music.Cover`, optional): Список обложек артиста.
        description (:obj:`str`, optional): Текстовое описание артиста.
        artist_type (:obj:`str`, optional): Тип артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    likes_count: Optional[int] = None
    stats: Optional['Stats'] = None
    trailer: Optional['ArtistTrailerStatus'] = None
    covers: Optional[List['Cover']] = None
    description: Optional[str] = None
    artist_type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist,)
