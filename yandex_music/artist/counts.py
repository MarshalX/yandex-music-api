from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Counts(YandexMusicModel):
    """Класс, представляющий счётчик некоторых значений исполнителя.

    Note:
        Под дополнительными подразумеваются треки и альбомы, в которых артист задействован, но не является его автором.
        Так же в дополнительные альбомы входят сборники.

    Attributes:
        tracks (:obj:`int`): Количество треков.
        direct_albums (:obj:`int`): Количество альбомов.
        also_albums (:obj:`int`): Количество дополнительных треков.
        also_tracks (:obj:`int`): Количество дополнительных альбомов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tracks: int
    direct_albums: int
    also_albums: int
    also_tracks: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.tracks, self.direct_albums, self.also_albums, self.also_tracks)
