import pytest

from yandex_music import TrackShort


@pytest.fixture(scope='class')
def track_short():
    return TrackShort(TestTrackShort.id, TestTrackShort.timestamp, TestTrackShort.album_id)


class TestTrackShort:
    timestamp = None
    album_id = None

    def test_expected_values(self, track_short, id):
        assert track_short.id == id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id

    def test_de_json_required(self, client, id):
        json_dict = {'id': id, 'timestamp': self.timestamp}
        track_short = TrackShort.de_json(json_dict, client)

        assert track_short.id == id
        assert track_short.timestamp == self.timestamp

    def test_de_json_all(self, client, id):
        json_dict = {'id': id, 'timestamp': self.timestamp, 'album_id': self.album_id}
        track_short = TrackShort.de_json(json_dict, client)

        assert track_short.id == id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id

    def test_equality(self):
        pass
