from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Playlist

from yandex_music import YandexMusicObject


class GeneratedPlaylist(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 ready: bool,
                 notify: bool,
                 data: Optional['Playlist'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.ready = ready
        self.notify = notify
        self.data = data

        self.client = client
        self._id_attrs = (self.type, self.ready, self.notify, self.data)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['GeneratedPlaylist']:
        if not data:
            return None

        data = super(GeneratedPlaylist, cls).de_json(data, client)
        from yandex_music import Playlist
        data['data'] = Playlist.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['GeneratedPlaylist']:
        if not data:
            return []

        generated_playlists = list()
        for generated_playlist in data:
            generated_playlists.append(cls.de_json(generated_playlist, client))

        return generated_playlists
