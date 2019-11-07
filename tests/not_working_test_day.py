import pytest

from yandex_music import Day


@pytest.fixture(scope='class')
def day(events, tracks_to_play_with_ads, tracks_to_play):
    return Day(TestDay.day, events, tracks_to_play_with_ads, tracks_to_play)


class TestDay:
    day = None

    def test_expected_values(self, day, events, tracks_to_play_with_ads, tracks_to_play):
        assert day.day == self.day
        assert day.events == events
        assert day.tracks_to_play_with_ads == tracks_to_play_with_ads
        assert day.tracks_to_play == tracks_to_play

    def test_de_json_required(self, client, events, tracks_to_play_with_ads, tracks_to_play):
        json_dict = {'day': self.day, 'events': events, 'tracks_to_play_with_ads': tracks_to_play_with_ads,
                     'tracks_to_play': tracks_to_play}
        day = Day.de_json(json_dict, client)

        assert day.day == self.day
        assert day.events == events
        assert day.tracks_to_play_with_ads == tracks_to_play_with_ads
        assert day.tracks_to_play == tracks_to_play

    def test_de_json_all(self, client, events, tracks_to_play_with_ads, tracks_to_play):
        json_dict = {'day': self.day, 'events': events, 'tracks_to_play_with_ads': tracks_to_play_with_ads,
                     'tracks_to_play': tracks_to_play}
        day = Day.de_json(json_dict, client)

        assert day.day == self.day
        assert day.events == events
        assert day.tracks_to_play_with_ads == tracks_to_play_with_ads
        assert day.tracks_to_play == tracks_to_play

    def test_equality(self):
        pass
