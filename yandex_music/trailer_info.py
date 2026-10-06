from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.track.track import Track


@model
class TrailerInfo(YandexMusicModel):
    """Класс, представляющий информацию о трейлере.

    Attributes:
        title (:obj:`str`, optional): Заголовок трейлера.
        tracks (:obj:`list` из :obj:`yandex_music.Track`, optional): Список треков трейлера.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    tracks: Optional[List['Track']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.tracks)
