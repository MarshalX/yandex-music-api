import pytest

from yandex_music import Feed


@pytest.fixture(scope='class')
def feed(generated_playlist, day):
    return Feed(
        TestFeed.can_get_more_events,
        TestFeed.pumpkin,
        TestFeed.is_wizard_passed,
        [generated_playlist],
        TestFeed.headlines,
        TestFeed.today,
        [day],
        TestFeed.next_revision,
    )


class TestFeed:
    can_get_more_events = True
    pumpkin = False
    is_wizard_passed = True
    headlines = []
    today = '2019-11-09'
    next_revision = '2019-11-08'

    def test_expected_values(self, feed, generated_playlist, day):
        assert feed.can_get_more_events == self.can_get_more_events
        assert feed.pumpkin == self.pumpkin
        assert feed.is_wizard_passed == self.is_wizard_passed
        assert feed.generated_playlists == [generated_playlist]
        assert feed.headlines == self.headlines
        assert feed.today == self.today
        assert feed.days == [day]
        assert feed.next_revision == self.next_revision

    def test_de_json_none(self, client):
        assert Feed.de_json({}, client) is None

    def test_de_json_required(self, client, generated_playlist, day):
        json_dict = {
            'can_get_more_events': self.can_get_more_events,
            'pumpkin': self.pumpkin,
            'is_wizard_passed': self.is_wizard_passed,
            'generated_playlists': [generated_playlist.to_dict()],
            'headlines': self.headlines,
            'today': self.today,
            'days': [day.to_dict()],
        }
        feed = Feed.de_json(json_dict, client)

        assert feed.can_get_more_events == self.can_get_more_events
        assert feed.pumpkin == self.pumpkin
        assert feed.is_wizard_passed == self.is_wizard_passed
        assert feed.generated_playlists == [generated_playlist]
        assert feed.headlines == self.headlines
        assert feed.today == self.today
        assert feed.days == [day]

    def test_de_json_all(self, client, generated_playlist, day):
        json_dict = {
            'can_get_more_events': self.can_get_more_events,
            'pumpkin': self.pumpkin,
            'is_wizard_passed': self.is_wizard_passed,
            'generated_playlists': [generated_playlist.to_dict()],
            'headlines': self.headlines,
            'today': self.today,
            'days': [day.to_dict()],
            'next_revision': self.next_revision,
        }
        feed = Feed.de_json(json_dict, client)

        assert feed.can_get_more_events == self.can_get_more_events
        assert feed.pumpkin == self.pumpkin
        assert feed.is_wizard_passed == self.is_wizard_passed
        assert feed.generated_playlists == [generated_playlist]
        assert feed.headlines == self.headlines
        assert feed.today == self.today
        assert feed.days == [day]
        assert feed.next_revision == self.next_revision

    def test_equality(self, generated_playlist, day):
        a = Feed(
            self.can_get_more_events,
            self.pumpkin,
            self.is_wizard_passed,
            [generated_playlist],
            self.headlines,
            self.today,
            [day],
        )
        b = Feed(False, self.pumpkin, self.is_wizard_passed, [], self.headlines, self.today, [day])
        c = Feed(
            self.can_get_more_events,
            self.pumpkin,
            self.is_wizard_passed,
            [generated_playlist],
            self.headlines,
            self.today,
            [day],
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
