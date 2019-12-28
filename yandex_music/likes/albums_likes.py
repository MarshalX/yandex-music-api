from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Album

from yandex_music import YandexMusicObject


class AlbumsLikes(YandexMusicObject):
    def __init__(self,
                 timestamp: str,
                 id_: Optional[int] = None,
                 album: Optional['Album'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.album = album
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.id, self.album)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AlbumsLikes']:
        if not data:
            return None

        data = super(AlbumsLikes, cls).de_json(data, client)
        from yandex_music import Album
        data['album'] = Album.de_json(data.get('album'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['AlbumsLikes']:
        if not data:
            return []

        albums_likes = list()
        for album_like in data:
            albums_likes.append(cls.de_json(album_like, client))

        return albums_likes
