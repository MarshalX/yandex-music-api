from typing import Dict

from yandex_music import Client, JSONType, TrackId, TrackShortOld


class TestTrackShortOld:
    timestamp = '2019-11-07T19:50:44+00:00'

    def test_expected_values(self, track_short_old: TrackShortOld, track_id: TrackId) -> None:
        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_de_json_none(self, client: Client) -> None:
        assert TrackShortOld.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert TrackShortOld.de_list([], client) == []

    def test_de_json_required(self, client: Client, track_id: TrackId) -> None:
        json_dict: Dict[str, JSONType] = {'track_id': track_id.to_dict(), 'timestamp': self.timestamp}
        track_short_old = TrackShortOld.de_json(json_dict, client)
        assert track_short_old is not None

        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_de_json_all(self, client: Client, track_id: TrackId) -> None:
        json_dict: Dict[str, JSONType] = {'track_id': track_id.to_dict(), 'timestamp': self.timestamp}
        track_short_old = TrackShortOld.de_json(json_dict, client)
        assert track_short_old is not None

        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_equality(self, track_id: TrackId) -> None:
        a = TrackShortOld(track_id, self.timestamp)
        b = TrackShortOld(track_id, self.timestamp)

        assert a == b
        assert hash(a) == hash(b)
        assert a != track_id
