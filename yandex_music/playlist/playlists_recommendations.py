from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track


class PlaylistsRecommendations(YandexMusicObject):
    def __init__(self,
                 tracks: List['Track'],
                 batch_id: str = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.batchId = batch_id
        self.tracks = tracks

        self.client = client
        self._id_attrs = (self.batchId, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlaylistsRecommendations']:
        if not data:
            return None

        data = super(PlaylistsRecommendations, cls).de_json(data, client)
        from yandex_music import Track
        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
