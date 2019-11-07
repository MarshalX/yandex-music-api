import pytest

from yandex_music import Dashboard


@pytest.fixture(scope='class')
def dashboard(stations):
    return Dashboard(TestDashboard.dashboard_id, stations, TestDashboard.pumpkin)


class TestDashboard:
    dashboard_id = None
    pumpkin = None

    def test_expected_values(self, dashboard, stations):
        assert dashboard.dashboard_id == self.dashboard_id
        assert dashboard.stations == stations
        assert dashboard.pumpkin == self.pumpkin

    def test_de_json_required(self, client, stations):
        json_dict = {'dashboard_id': self.dashboard_id, 'stations': stations, 'pumpkin': self.pumpkin}
        dashboard = Dashboard.de_json(json_dict, client)

        assert dashboard.dashboard_id == self.dashboard_id
        assert dashboard.stations == stations
        assert dashboard.pumpkin == self.pumpkin

    def test_de_json_all(self, client, stations):
        json_dict = {'dashboard_id': self.dashboard_id, 'stations': stations, 'pumpkin': self.pumpkin}
        dashboard = Dashboard.de_json(json_dict, client)

        assert dashboard.dashboard_id == self.dashboard_id
        assert dashboard.stations == stations
        assert dashboard.pumpkin == self.pumpkin

    def test_equality(self):
        pass
