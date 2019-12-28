from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Album, Track

from yandex_music import YandexMusicObject


class AlbumEvent(YandexMusicObject):
    def __init__(self,
                 album: Optional['Album'],
                 tracks: List['Track'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.album = album
        self.tracks = tracks

        self.client = client
        self._id_attrs = (self.album, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AlbumEvent']:
        if not data:
            return None

        data = super(AlbumEvent, cls).de_json(data, client)
        from yandex_music import Album, Track
        data['album'] = Album.de_json(data.get('album'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['AlbumEvent']:
        if not data:
            return []

        album_events = list()
        for album_event in data:
            album_events.append(cls.de_json(album_event, client))

        return album_events
