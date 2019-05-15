from datetime import datetime

from yandex_music import YandexMusicObject


class Day(YandexMusicObject):
    def __init__(self,
                 day,
                 events,
                 tracks_to_play_with_ads,
                 tracks_to_play,
                 client=None,
                 **kwargs):
        self.day = datetime.fromisoformat(day)
        self.events = events
        self.tracks_to_play_with_ads = tracks_to_play_with_ads
        self.tracks_to_play = tracks_to_play

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Day, cls).de_json(data, client)
        from yandex_music import Event, Track, TrackWithAds
        data['events'] = Event.de_list(data.get('events'), client)
        data['tracks_to_play_with_ads'] = TrackWithAds.de_list(data.get('tracks_to_play_with_ads'), client)
        data['tracks_to_play'] = Track.de_list(data.get('tracks_to_play'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        days = list()
        for day in data:
            days.append(cls.de_json(day, client))

        return days
