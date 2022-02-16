from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Album, Track


@model
class AlbumEvent(YandexMusicObject):
    """Класс, представляющий альбом в событии фида.

    Attributes:
        album (:obj:`yandex_music.Album` | :obj:`None`): Альбом.
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional['Album']
    tracks: List['Track']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.album, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AlbumEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.AlbumEvent`: Альбом в событии фида.
        """
        if not data:
            return None

        data = super(AlbumEvent, cls).de_json(data, client)
        from yandex_music import Album, Track

        data['album'] = Album.de_json(data.get('album'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['AlbumEvent']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.AlbumEvent`: Альбомы в событии фида.
        """
        if not data:
            return []

        album_events = list()
        for album_event in data:
            album_events.append(cls.de_json(album_event, client))

        return album_events
