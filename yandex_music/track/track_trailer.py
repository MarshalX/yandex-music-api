from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.track.track import Track


@model
class TrackTrailer(YandexMusicModel):
    """Класс, представляющий трейлер трека.

    Attributes:
        title (:obj:`str`, optional): Заголовок трейлера.
        track (:obj:`yandex_music.Track`, optional): Трек.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    track: Optional['Track'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.track)
