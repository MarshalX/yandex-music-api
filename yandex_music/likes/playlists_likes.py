from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Playlist

from yandex_music import YandexMusicObject


class PlaylistsLikes(YandexMusicObject):
    def __init__(self,
                 timestamp: str,
                 id_=None,
                 playlist: Optional['Playlist'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.playlist = playlist
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.id, self.playlist)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlaylistsLikes']:
        if not data:
            return None

        data = super(PlaylistsLikes, cls).de_json(data, client)
        from yandex_music import Playlist
        data['playlist'] = Playlist.de_json(data.get('playlist'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['PlaylistsLikes']:
        if not data:
            return []

        playlists_likes = list()
        for playlist_like in data:
            playlists_likes.append(cls.de_json(playlist_like, client))

        return playlists_likes
