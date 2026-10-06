from typing import Dict

from yandex_music import Client, Day, Event, JSONType, Track, TrackWithAds


class TestDay:
    day = '2019-11-09'

    def test_expected_values(self, day: Day, event: Event, track_with_ads: TrackWithAds, track: Track) -> None:
        assert day.day == self.day
        assert day.events == [event]
        assert day.tracks_to_play_with_ads == [track_with_ads]
        assert day.tracks_to_play == [track]

    def test_de_json_none(self, client: Client) -> None:
        assert Day.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Day.de_list([], client) == []

    def test_de_json_required(self, client: Client, event: Event, track_with_ads: TrackWithAds, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'day': self.day,
            'events': [event.to_dict()],
            'tracks_to_play_with_ads': [track_with_ads.to_dict()],
            'tracks_to_play': [track.to_dict()],
        }
        day = Day.de_json(json_dict, client)
        assert day is not None

        assert day.day == self.day
        assert day.events == [event]
        assert day.tracks_to_play_with_ads == [track_with_ads]
        assert day.tracks_to_play == [track]

    def test_de_json_all(self, client: Client, event: Event, track_with_ads: TrackWithAds, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'day': self.day,
            'events': [event.to_dict()],
            'tracks_to_play_with_ads': [track_with_ads.to_dict()],
            'tracks_to_play': [track.to_dict()],
        }
        day = Day.de_json(json_dict, client)
        assert day is not None

        assert day.day == self.day
        assert day.events == [event]
        assert day.tracks_to_play_with_ads == [track_with_ads]
        assert day.tracks_to_play == [track]

    def test_equality(self, event: Event, track_with_ads: TrackWithAds, track: Track) -> None:
        a = Day(self.day, [event], [track_with_ads], [track])
        b = Day('', [event], [track_with_ads], [track])
        c = Day(self.day, [event], [track_with_ads], [track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
