from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Album, ClientType, JSONType, Track


@model
class AlbumEvent(YandexMusicModel):
    """Класс, представляющий альбом в событии фида.

    Attributes:
        album (:obj:`yandex_music.Album`, optional): Альбом.
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional['Album']
    tracks: List['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.album, self.tracks)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['AlbumEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.AlbumEvent`: Альбом в событии фида.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Album, Track

        cls_data['album'] = Album.de_json(data.get('album'), client)
        cls_data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **cls_data)  # type: ignore
