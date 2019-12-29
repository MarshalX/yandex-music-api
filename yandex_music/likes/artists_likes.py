from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Artist

from yandex_music import YandexMusicObject


class ArtistsLikes(YandexMusicObject):
    def __init__(self,
                 id_=None,
                 artist: Optional['Artist'] = None,
                 timestamp: str = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.artist = artist
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.id, self.artist)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistsLikes']:
        if not data:
            return None

        data = super(ArtistsLikes, cls).de_json(data, client)
        from yandex_music import Artist
        if 'artist' not in data:
            temp_data = data.copy()
            data.clear()
            data['artist'] = Artist.de_json(temp_data, client)
        else:
            data['artist'] = Artist.de_json(data.get('artist'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['ArtistsLikes']:
        if not data:
            return []

        artists_likes = list()
        for artist_like in data:
            artists_likes.append(cls.de_json(artist_like, client))

        return artists_likes
