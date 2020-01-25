from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Track

from yandex_music import YandexMusicObject


class TracksSimilar(YandexMusicObject):
    def __init__(self,
                 track: Optional['Track'],
                 similar_tracks: List['Track'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.track = track
        self.similar_tracks = similar_tracks

        self.client = client
        self._id_attrs = (self.track, self.similar_tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TracksSimilar']:
        if not data:
            return None

        data = super(TracksSimilar, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)
        data['similar_tracks'] = Track.de_list(data.get('similar_tracks'), client)

        return cls(client=client, **data)
