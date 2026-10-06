from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.album.album import Album


@model
class Presaves(YandexMusicModel):
    """Класс, представляющий список предсохранённых альбомов.

    Attributes:
        upcoming_albums (:obj:`list` из :obj:`yandex_music.Album`, optional): Список предстоящих альбомов.
        released_albums (:obj:`list` из :obj:`yandex_music.Album`, optional): Список вышедших альбомов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    upcoming_albums: Optional[List['Album']] = None
    released_albums: Optional[List['Album']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.upcoming_albums, self.released_albums)
