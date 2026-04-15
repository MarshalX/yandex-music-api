from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Album, Artist, ClientType, JSONType, Playlist, Wave


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MusicHistoryContextFullModel']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MusicHistoryContextFullModel`: Полная модель контекста истории прослушивания.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Album, Artist, Playlist, Wave

        cls_data['album'] = Album.de_json(cls_data.get('album'), client)
        cls_data['artist'] = Artist.de_json(cls_data.get('artist'), client)
        cls_data['playlist'] = Playlist.de_json(cls_data.get('playlist'), client)
        cls_data['wave'] = Wave.de_json(cls_data.get('wave'), client)
        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)

        return cls(client=client, **cls_data)
