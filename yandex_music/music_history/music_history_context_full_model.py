from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Album, Artist, ClientType, Playlist, Wave


@model
class MusicHistoryContextFullModel(YandexMusicModel):
    """Класс, представляющий полную модель контекста истории прослушивания.

    Note:
        Набор заполненных полей зависит от типа контекста:

        - ``album``: `album`, `artists`, `available`.
        - ``artist``: `artist`, `available`.
        - ``playlist``: `playlist`, `available`, `tracks_count`.
        - ``wave``: `wave`, `simple_wave_foreground_image_url`, `simple_wave_background_color`.

    Attributes:
        album (:obj:`yandex_music.Album`, optional): Альбом контекста.
        artist (:obj:`yandex_music.Artist`, optional): Исполнитель контекста.
        playlist (:obj:`yandex_music.Playlist`, optional): Плейлист контекста.
        wave (:obj:`yandex_music.Wave`, optional): Волна контекста.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список исполнителей (для альбома).
        available (:obj:`bool`, optional): Доступность.
        tracks_count (:obj:`int`, optional): Количество треков (для плейлиста).
        simple_wave_foreground_image_url (:obj:`str`, optional): URL изображения волны.
        simple_wave_background_color (:obj:`str`, optional): Цвет фона волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional['Album'] = None
    artist: Optional['Artist'] = None
    playlist: Optional['Playlist'] = None
    wave: Optional['Wave'] = None
    artists: Optional[List['Artist']] = None
    available: Optional[bool] = None
    tracks_count: Optional[int] = None
    simple_wave_foreground_image_url: Optional[str] = None
    simple_wave_background_color: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.album, self.artist, self.playlist, self.wave)
