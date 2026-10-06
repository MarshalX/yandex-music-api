from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist import Artist
    from yandex_music.clip.clip import Clip


@model
class ArtistClipData(YandexMusicModel):
    """Класс, представляющий данные клипа артиста.

    Attributes:
        clip (:obj:`yandex_music.Clip`, optional): Клип.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов клипа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    clip: Optional['Clip'] = None
    artists: Optional[List['Artist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.clip,)
