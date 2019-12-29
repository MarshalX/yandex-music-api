import pytest

from yandex_music import TrackShort


@pytest.fixture(scope='class')
def track_short():
    return TrackShort(TestTrackShort.id, TestTrackShort.timestamp, TestTrackShort.album_id)


class TestTrackShort:
    id = 21997388
    timestamp = '2019-11-07T03:00:00+00:00'
    album_id = None

    def test_expected_values(self, track_short):
        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id

    def test_de_json_none(self, client):
        assert TrackShort.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert TrackShort.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'id_': self.id, 'timestamp': self.timestamp}
        track_short = TrackShort.de_json(json_dict, client)

        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp

    def test_de_json_all(self, client):
        json_dict = {'id_': self.id, 'timestamp': self.timestamp, 'album_id': self.album_id}
        track_short = TrackShort.de_json(json_dict, client)

        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id

    def test_equality(self):
        a = TrackShort(self.id, self.timestamp, self.album_id)
        b = TrackShort(23, self.timestamp, self.album_id)
        c = TrackShort(self.id, self.timestamp)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
