import pytest

from yandex_music import TrackWithAds


@pytest.fixture(scope='class')
def track_with_ads(track):
    return TrackWithAds(TestTrackWithAds.type, track)


class TestTrackWithAds:
    type = None

    def test_expected_values(self, track_with_ads, track):
        assert track_with_ads.type == self.type
        assert track_with_ads.track == track

    def test_de_json_required(self, client, track):
        json_dict = {'type': self.type, 'track': track}
        track_with_ads = TrackWithAds.de_json(json_dict, client)

        assert track_with_ads.type == self.type
        assert track_with_ads.track == track

    def test_de_json_all(self, client, track):
        json_dict = {'type': self.type, 'track': track}
        track_with_ads = TrackWithAds.de_json(json_dict, client)

        assert track_with_ads.type == self.type
        assert track_with_ads.track == track

    def test_equality(self):
        pass
