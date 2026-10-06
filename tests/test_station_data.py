from typing import Dict

from yandex_music import Client, JSONType, StationData


class TestStationData:
    name = "Marshal's station"

    def test_expected_values(self, station_data: StationData) -> None:
        assert station_data.name == self.name

    def test_de_json_none(self, client: Client) -> None:
        assert StationData.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'name': self.name}
        station_data = StationData.de_json(json_dict, client)
        assert station_data is not None

        assert station_data.name == self.name

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'name': self.name}
        station_data = StationData.de_json(json_dict, client)
        assert station_data is not None

        assert station_data.name == self.name

    def test_equality(self) -> None:
        a = StationData(self.name)
        b = StationData('')
        c = StationData(self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
