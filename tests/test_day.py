from yandex_music import Day


class TestDay:
    day = '2019-11-09'

    def test_expected_values(self, day, event, track_with_ads, track):
        assert day.day == self.day
        assert day.events == [event]
        assert day.tracks_to_play_with_ads == [track_with_ads]
        assert day.tracks_to_play == [track]

    def test_de_json_none(self, client):
        assert Day.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Day.de_list({}, client) == []

    def test_de_json_required(self, client, event, track_with_ads, track):
        json_dict = {
            'day': self.day,
            'events': [event.to_dict()],
            'tracks_to_play_with_ads': [track_with_ads.to_dict()],
            'tracks_to_play': [track.to_dict()],
        }
        day = Day.de_json(json_dict, client)

        assert day.day == self.day
        assert day.events == [event]
        assert day.tracks_to_play_with_ads == [track_with_ads]
        assert day.tracks_to_play == [track]

    def test_de_json_all(self, client, event, track_with_ads, track):
        json_dict = {
            'day': self.day,
            'events': [event.to_dict()],
            'tracks_to_play_with_ads': [track_with_ads.to_dict()],
            'tracks_to_play': [track.to_dict()],
        }
        day = Day.de_json(json_dict, client)

        assert day.day == self.day
        assert day.events == [event]
        assert day.tracks_to_play_with_ads == [track_with_ads]
        assert day.tracks_to_play == [track]

    def test_equality(self, event, track_with_ads, track):
        a = Day(self.day, [event], [track_with_ads], [track])
        b = Day('', [event], [track_with_ads], [track])
        c = Day(self.day, [event], [track_with_ads], [track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
