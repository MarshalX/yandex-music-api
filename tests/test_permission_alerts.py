import pytest

from yandex_music import PermissionAlerts


@pytest.fixture(scope='class')
def permission_alerts():
    return PermissionAlerts(TestPermissionAlerts.alerts)


class TestPermissionAlerts:
    alerts = []

    def test_expected_values(self, permission_alerts):
        assert permission_alerts.alerts == self.alerts

    def test_de_json_none(self, client):
        assert PermissionAlerts.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'alerts': self.alerts}
        permission_alerts = PermissionAlerts.de_json(json_dict, client)

        assert permission_alerts.alerts == self.alerts

    def test_de_json_all(self, client):
        json_dict = {'alerts': self.alerts}
        permission_alerts = PermissionAlerts.de_json(json_dict, client)

        assert permission_alerts.alerts == self.alerts

    def test_equality(self, permissions):
        a = PermissionAlerts([])

        assert a != permissions
        assert hash(a) != hash(permissions)
        assert a is not permissions
