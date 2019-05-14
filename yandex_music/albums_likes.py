from datetime import datetime

from yandex_music import YandexMusicObject


class AlbumsLikes(YandexMusicObject):
    def __init__(self,
                 timestamp,
                 id=None,
                 album=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.album = album
        self.timestamp = datetime.fromisoformat(timestamp)

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(AlbumsLikes, cls).de_json(data, client)
        from yandex_music import Album
        data['album'] = Album.de_json(data.get('album'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        albums_likes = list()
        for album_like in data:
            albums_likes.append(cls.de_json(album_like, client))

        return albums_likes
