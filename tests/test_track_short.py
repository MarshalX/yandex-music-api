from typing import Dict, Optional

import pytest

from yandex_music import Chart, Client, JSONType, Track, TrackShort


@pytest.fixture(scope='class')
def track_short(track: Track, chart: Chart) -> TrackShort:
    return TrackShort(
        TestTrackShort.id,
        TestTrackShort.timestamp,
        TestTrackShort.album_id,
        TestTrackShort.play_count,
        TestTrackShort.recent,
        chart,
        track,
        TestTrackShort.original_index,
        TestTrackShort.original_shuffle_index,
    )


class TestTrackShort:
    id = 21997388
    timestamp = '2019-11-07T03:00:00+00:00'
    album_id: Optional[str] = None
    play_count = 0
    recent = False
    original_index = 23
    original_shuffle_index = 7

    def test_expected_values(self, track_short: TrackShort, track: Track, chart: Chart) -> None:
        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id
        assert track_short.play_count == self.play_count
        assert track_short.recent == self.recent
        assert track_short.track == track
        assert track_short.chart == chart
        assert track_short.original_index == self.original_index
        assert track_short.original_shuffle_index == self.original_shuffle_index

    def test_de_json_none(self, client: Client) -> None:
        assert TrackShort.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert TrackShort.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id, 'timestamp': self.timestamp}
        track_short = TrackShort.de_json(json_dict, client)
        assert track_short is not None

        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp

    def test_de_json_all(self, client: Client, track: Track, chart: Chart) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'timestamp': self.timestamp,
            'album_id': self.album_id,
            'play_count': self.play_count,
            'recent': self.recent,
            'track': track.to_dict(),
            'chart': chart.to_dict(),
            'original_index': self.original_index,
            'originalShuffleIndex': self.original_shuffle_index,
        }
        track_short = TrackShort.de_json(json_dict, client)
        assert track_short is not None

        assert track_short.id == self.id
        assert track_short.timestamp == self.timestamp
        assert track_short.album_id == self.album_id
        assert track_short.play_count == self.play_count
        assert track_short.recent == self.recent
        assert track_short.track == track
        assert track_short.chart == chart
        assert track_short.original_index == self.original_index
        assert track_short.original_shuffle_index == self.original_shuffle_index

    def test_equality(self) -> None:
        a = TrackShort(self.id, self.timestamp, self.album_id)
        b = TrackShort(23, self.timestamp, self.album_id)
        c = TrackShort(self.id, self.timestamp)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
