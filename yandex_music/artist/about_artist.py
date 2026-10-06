from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist import Artist
    from yandex_music.artist.artist_link import ArtistLink
    from yandex_music.artist.stats import Stats
    from yandex_music.cover import Cover


@model
class ArtistAbout(YandexMusicModel):
    """Класс, представляющий информацию «Об артисте».

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        stats (:obj:`yandex_music.Stats`, optional): Статистика прослушиваний.
        description (:obj:`str`, optional): Текстовое описание артиста.
        links (:obj:`list` из :obj:`yandex_music.ArtistLink`, optional): Ссылки на внешние ресурсы.
        covers (:obj:`list` из :obj:`yandex_music.Cover`, optional): Список обложек артиста.
        artist_type (:obj:`str`, optional): Тип артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    stats: Optional['Stats'] = None
    description: Optional[str] = None
    links: Optional[List['ArtistLink']] = None
    covers: Optional[List['Cover']] = None
    artist_type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist,)
