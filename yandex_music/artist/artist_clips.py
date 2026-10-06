from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist_clip_item import ArtistClipItem
    from yandex_music.pager import Pager


@model
class ArtistClips(YandexMusicModel):
    """Класс, представляющий блок клипов артиста.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ArtistClipItem`, optional): Список элементов клипов.
        pager (:obj:`yandex_music.Pager`, optional): Пагинация.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: Optional[List['ArtistClipItem']] = None
    pager: Optional['Pager'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items, self.pager)
