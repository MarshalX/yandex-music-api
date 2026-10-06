from typing import Dict

import pytest

from yandex_music import Client, Dashboard, JSONType, StationResult


@pytest.fixture(scope='class')
def dashboard(station_result: StationResult) -> Dashboard:
    return Dashboard(TestDashboard.dashboard_id, [station_result], TestDashboard.pumpkin)


class TestDashboard:
    dashboard_id = '1573229923780896-4168369461406125948'
    pumpkin = False

    def test_expected_values(self, dashboard: Dashboard, station_result: StationResult) -> None:
        assert dashboard.dashboard_id == self.dashboard_id
        assert dashboard.stations == [station_result]
        assert dashboard.pumpkin == self.pumpkin

    def test_de_json_none(self, client: Client) -> None:
        assert Dashboard.de_json({}, client) is None

    def test_de_json_required(self, client: Client, station_result: StationResult) -> None:
        json_dict: Dict[str, JSONType] = {
            'dashboard_id': self.dashboard_id,
            'stations': [station_result.to_dict()],
            'pumpkin': self.pumpkin,
        }
        dashboard = Dashboard.de_json(json_dict, client)
        assert dashboard is not None

        assert dashboard.dashboard_id == self.dashboard_id
        assert dashboard.stations == [station_result]
        assert dashboard.pumpkin == self.pumpkin

    def test_de_json_all(self, client: Client, station_result: StationResult) -> None:
        json_dict: Dict[str, JSONType] = {
            'dashboard_id': self.dashboard_id,
            'stations': [station_result.to_dict()],
            'pumpkin': self.pumpkin,
        }
        dashboard = Dashboard.de_json(json_dict, client)
        assert dashboard is not None

        assert dashboard.dashboard_id == self.dashboard_id
        assert dashboard.stations == [station_result]
        assert dashboard.pumpkin == self.pumpkin

    def test_equality(self, station_result: StationResult) -> None:
        a = Dashboard(self.dashboard_id, [station_result], self.pumpkin)
        b = Dashboard('', [station_result], True)
        c = Dashboard(self.dashboard_id, [station_result], self.pumpkin)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
