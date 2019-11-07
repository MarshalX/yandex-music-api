import pytest

from yandex_music import Feed


@pytest.fixture(scope='class')
def feed(generated_playlists, days):
    return Feed(TestFeed.can_get_more_events, TestFeed.pumpkin, TestFeed.is_wizard_passed, generated_playlists,
                TestFeed.headlines, TestFeed.today, days, TestFeed.next_revision)


class TestFeed:
    can_get_more_events = None
    pumpkin = None
    is_wizard_passed = None
    headlines = None
    today = None
    next_revision = None

    def test_expected_values(self, feed, generated_playlists, days):
        assert feed.can_get_more_events == self.can_get_more_events
        assert feed.pumpkin == self.pumpkin
        assert feed.is_wizard_passed == self.is_wizard_passed
        assert feed.generated_playlists == generated_playlists
        assert feed.headlines == self.headlines
        assert feed.today == self.today
        assert feed.days == days
        assert feed.next_revision == self.next_revision

    def test_de_json_required(self, client, generated_playlists, days):
        json_dict = {'can_get_more_events': self.can_get_more_events, 'pumpkin': self.pumpkin,
                     'is_wizard_passed': self.is_wizard_passed, 'generated_playlists': generated_playlists,
                     'headlines': self.headlines, 'today': self.today, 'days': days}
        feed = Feed.de_json(json_dict, client)

        assert feed.can_get_more_events == self.can_get_more_events
        assert feed.pumpkin == self.pumpkin
        assert feed.is_wizard_passed == self.is_wizard_passed
        assert feed.generated_playlists == generated_playlists
        assert feed.headlines == self.headlines
        assert feed.today == self.today
        assert feed.days == days

    def test_de_json_all(self, client, generated_playlists, days):
        json_dict = {'can_get_more_events': self.can_get_more_events, 'pumpkin': self.pumpkin,
                     'is_wizard_passed': self.is_wizard_passed, 'generated_playlists': generated_playlists,
                     'headlines': self.headlines, 'today': self.today, 'days': days,
                     'next_revision': self.next_revision}
        feed = Feed.de_json(json_dict, client)

        assert feed.can_get_more_events == self.can_get_more_events
        assert feed.pumpkin == self.pumpkin
        assert feed.is_wizard_passed == self.is_wizard_passed
        assert feed.generated_playlists == generated_playlists
        assert feed.headlines == self.headlines
        assert feed.today == self.today
        assert feed.days == days
        assert feed.next_revision == self.next_revision

    def test_equality(self):
        pass
