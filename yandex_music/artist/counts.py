from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Counts(YandexMusicObject):
    def __init__(self,
                 tracks,
                 direct_albums,
                 also_albums,
                 also_tracks,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.tracks = tracks
        self.direct_albums = direct_albums
        self.also_albums = also_albums
        self.also_tracks = also_tracks

        self.client = client
        self._id_attrs = (self.tracks, self.direct_albums, self.also_albums, self.also_tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client'):
        if not data:
            return None

        data = super(Counts, cls).de_json(data, client)

        return cls(client=client, **data)
