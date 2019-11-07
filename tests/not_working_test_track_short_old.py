import pytest

from yandex_music import TrackShortOld


@pytest.fixture(scope='class')
def track_short_old(track_id):
    return TrackShortOld(track_id, TestTrackShortOld.timestamp)


class TestTrackShortOld:
    timestamp = None

    def test_expected_values(self, track_short_old, track_id):
        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_de_json_required(self, client, track_id):
        json_dict = {'track_id': track_id, 'timestamp': self.timestamp}
        track_short_old = TrackShortOld.de_json(json_dict, client)

        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_de_json_all(self, client, track_id):
        json_dict = {'track_id': track_id, 'timestamp': self.timestamp}
        track_short_old = TrackShortOld.de_json(json_dict, client)

        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_equality(self):
        pass
