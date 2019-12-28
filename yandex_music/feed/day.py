from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Event, Track, TrackWithAds

from yandex_music import YandexMusicObject


class Day(YandexMusicObject):
    def __init__(self,
                 day: str,
                 events: List['Event'],
                 tracks_to_play_with_ads: List['TrackWithAds'],
                 tracks_to_play: List['Track'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.day = day
        self.events = events
        self.tracks_to_play_with_ads = tracks_to_play_with_ads
        self.tracks_to_play = tracks_to_play

        self.client = client
        self._id_attrs = (self.day, self.events, self.tracks_to_play_with_ads, self.tracks_to_play)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Day']:
        if not data:
            return None

        data = super(Day, cls).de_json(data, client)
        from yandex_music import Event, Track, TrackWithAds
        data['events'] = Event.de_list(data.get('events'), client)
        data['tracks_to_play_with_ads'] = TrackWithAds.de_list(data.get('tracks_to_play_with_ads'), client)
        data['tracks_to_play'] = Track.de_list(data.get('tracks_to_play'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Day']:
        if not data:
            return []

        days = list()
        for day in data:
            days.append(cls.de_json(day, client))

        return days
