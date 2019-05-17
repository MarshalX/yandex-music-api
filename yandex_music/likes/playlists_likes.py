from datetime import datetime

from yandex_music import YandexMusicObject


class PlaylistsLikes(YandexMusicObject):
    def __init__(self,
                 timestamp,
                 id=None,
                 playlist=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.playlist = playlist
        self.timestamp = datetime.fromisoformat(timestamp)

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PlaylistsLikes, cls).de_json(data, client)
        from yandex_music import Playlist
        data['playlist'] = Playlist.de_json(data.get('playlist'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        playlists_likes = list()
        for playlist_like in data:
            playlists_likes.append(cls.de_json(playlist_like, client))

        return playlists_likes
