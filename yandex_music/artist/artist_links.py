from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist_link import ArtistLink


@model
class ArtistLinks(YandexMusicModel):
    """Класс, представляющий ссылки на страницы артиста.

    Attributes:
        links (:obj:`list` из :obj:`yandex_music.ArtistLink`, optional): Список ссылок.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    links: Optional[List['ArtistLink']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.links,)
