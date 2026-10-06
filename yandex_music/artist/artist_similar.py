from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist import Artist


@model
class ArtistSimilar(YandexMusicModel):
    """Класс, представляющий похожих артистов.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист, для которого найдены похожие.
        similar_artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список похожих артистов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    similar_artists: Optional[List['Artist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist, self.similar_artists)
