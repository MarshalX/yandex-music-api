import pytest

from yandex_music import StationTracksResult


@pytest.fixture(scope='class')
def station_tracks_result(id_, sequence):
    return StationTracksResult(id_, [sequence], TestStationTracksResult.batch_id, TestStationTracksResult.pumpkin)


class TestStationTracksResult:
    batch_id = '1573227402825981-2727432063278102211'
    pumpkin = False

    def test_expected_values(self, station_tracks_result, id_, sequence):
        assert station_tracks_result.id == id_
        assert station_tracks_result.sequence == [sequence]
        assert station_tracks_result.batch_id == self.batch_id
        assert station_tracks_result.pumpkin == self.pumpkin

    def test_de_json_none(self, client):
        assert StationTracksResult.de_json({}, client) is None

    def test_de_json_required(self, client, id_, sequence):
        json_dict = {
            'id': id_.to_dict(),
            'sequence': [sequence.to_dict()],
            'batch_id': self.batch_id,
            'pumpkin': self.pumpkin,
        }
        station_tracks_result = StationTracksResult.de_json(json_dict, client)

        assert station_tracks_result.id == id_
        assert station_tracks_result.sequence == [sequence]
        assert station_tracks_result.batch_id == self.batch_id
        assert station_tracks_result.pumpkin == self.pumpkin

    def test_de_json_all(self, client, id_, sequence):
        json_dict = {
            'id': id_.to_dict(),
            'sequence': [sequence.to_dict()],
            'batch_id': self.batch_id,
            'pumpkin': self.pumpkin,
        }
        station_tracks_result = StationTracksResult.de_json(json_dict, client)

        assert station_tracks_result.id == id_
        assert station_tracks_result.sequence == [sequence]
        assert station_tracks_result.batch_id == self.batch_id
        assert station_tracks_result.pumpkin == self.pumpkin

    def test_equality(self, id_, sequence):
        a = StationTracksResult(id_, sequence, self.batch_id, self.pumpkin)
        b = StationTracksResult(id_, sequence, "", False)
        c = StationTracksResult(id_, sequence, self.batch_id, self.pumpkin)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
