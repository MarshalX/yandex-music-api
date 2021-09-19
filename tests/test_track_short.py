import pytest

from yandex_music import TrackShort


@pytest.fixture(scope='class')
def track_short(track, chart):
    return TrackShort(
        TestTrackShort.id,
        TestTrackShort.timestamp,
        TestTrackShort.album_id,
        TestTrackShort.play_count,
        TestTrackShort.recent,
        chart,
        track,
    )


class TestTrackShort:
    id = 21997388
    timestamp = '2019-11-07T03:00:00+00:00'
    album_id = None
    play_count = 0
    recent = False

    def test_expected_values(self, track_short, track, chart):
        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id
        assert track_short.play_count == self.play_count
        assert track_short.recent == self.recent
        assert track_short.track == track
        assert track_short.chart == chart

    def test_de_json_none(self, client):
        assert TrackShort.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert TrackShort.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'id': self.id, 'timestamp': self.timestamp}
        track_short = TrackShort.de_json(json_dict, client)

        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp

    def test_de_json_all(self, client, track, chart):
        json_dict = {
            'id': self.id,
            'timestamp': self.timestamp,
            'album_id': self.album_id,
            'play_count': self.play_count,
            'recent': self.recent,
            'track': track.to_dict(),
            'chart': chart.to_dict(),
        }
        track_short = TrackShort.de_json(json_dict, client)

        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id
        assert track_short.play_count == self.play_count
        assert track_short.recent == self.recent
        assert track_short.track == track
        assert track_short.chart == chart

    def test_equality(self):
        a = TrackShort(self.id, self.timestamp, self.album_id)
        b = TrackShort(23, self.timestamp, self.album_id)
        c = TrackShort(self.id, self.timestamp)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
