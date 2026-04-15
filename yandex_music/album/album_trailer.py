from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.album.album import Album
    from yandex_music.album.trailer_info import TrailerInfo
    from yandex_music.artist.artist import Artist


@model
class AlbumTrailer(YandexMusicModel):
    """Класс, представляющий трейлер альбома.

    Attributes:
        album (:obj:`yandex_music.Album`, optional): Альбом.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список артистов.
        trailer (:obj:`yandex_music.TrailerInfo`, optional): Информация о трейлере.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional['Album'] = None
    artists: Optional[List['Artist']] = None
    trailer: Optional['TrailerInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.album, self.trailer)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['AlbumTrailer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.AlbumTrailer`: Трейлер альбома.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Album, Artist
        from yandex_music.album.trailer_info import TrailerInfo

        cls_data['album'] = Album.de_json(cls_data.get('album'), client)
        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)
        cls_data['trailer'] = TrailerInfo.de_json(cls_data.get('trailer'), client)

        return cls(client=client, **cls_data)
