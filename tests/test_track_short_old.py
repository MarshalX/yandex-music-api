from yandex_music import TrackShortOld


class TestTrackShortOld:
    timestamp = '2019-11-07T19:50:44+00:00'

    def test_expected_values(self, track_short_old, track_id):
        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_de_json_none(self, client):
        assert TrackShortOld.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert TrackShortOld.de_list({}, client) == []

    def test_de_json_required(self, client, track_id):
        json_dict = {'track_id': track_id.to_dict(), 'timestamp': self.timestamp}
        track_short_old = TrackShortOld.de_json(json_dict, client)

        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_de_json_all(self, client, track_id):
        json_dict = {'track_id': track_id.to_dict(), 'timestamp': self.timestamp}
        track_short_old = TrackShortOld.de_json(json_dict, client)

        assert track_short_old.track_id == track_id
        assert track_short_old.timestamp == self.timestamp

    def test_equality(self, track_id):
        a = TrackShortOld(track_id, self.timestamp)
        b = TrackShortOld(track_id, self.timestamp)

        assert a == b
        assert hash(a) == hash(b)
        assert a != track_id
