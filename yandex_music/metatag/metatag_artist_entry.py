from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, Track


@model
class MetatagArtistEntry(YandexMusicModel):
    """Класс, представляющий запись артиста в списке метатега.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        popular_tracks (:obj:`list` из :obj:`yandex_music.Track`): Популярные треки артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    popular_tracks: List['Track'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist,)
