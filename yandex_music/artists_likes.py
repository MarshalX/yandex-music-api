from datetime import datetime

from yandex_music import YandexMusicObject


class ArtistsLikes(YandexMusicObject):
    def __init__(self,
                 id=None,
                 artist=None,
                 timestamp=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.artist = artist
        self.timestamp = datetime.fromisoformat(timestamp) if timestamp else timestamp

        self.client = client

    @classmethod
    def de_json(cls, data, client):
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
    def de_list(cls, data, client):
        if not data:
            return []

        artists_likes = list()
        for artist_like in data:
            artists_likes.append(cls.de_json(artist_like, client))

        return artists_likes
