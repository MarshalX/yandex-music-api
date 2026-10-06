from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist import Artist
    from yandex_music.trailer_info import TrailerInfo


@model
class ArtistTrailer(YandexMusicModel):
    """Класс, представляющий трейлер артиста.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        trailer (:obj:`yandex_music.TrailerInfo`, optional): Информация о трейлере.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    trailer: Optional['TrailerInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist, self.trailer)
