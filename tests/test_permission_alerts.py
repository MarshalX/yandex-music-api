from typing import Dict, List

import pytest

from yandex_music import Client, JSONType, PermissionAlerts, Permissions


@pytest.fixture(scope='class')
def permission_alerts() -> PermissionAlerts:
    return PermissionAlerts(TestPermissionAlerts.alerts)


class TestPermissionAlerts:
    alerts: List[str] = []

    def test_expected_values(self, permission_alerts: PermissionAlerts) -> None:
        assert permission_alerts.alerts == self.alerts

    def test_de_json_none(self, client: Client) -> None:
        assert PermissionAlerts.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'alerts': self.alerts}
        permission_alerts = PermissionAlerts.de_json(json_dict, client)
        assert permission_alerts is not None

        assert permission_alerts.alerts == self.alerts

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'alerts': self.alerts}
        permission_alerts = PermissionAlerts.de_json(json_dict, client)
        assert permission_alerts is not None

        assert permission_alerts.alerts == self.alerts

    def test_equality(self, permissions: Permissions) -> None:
        a = PermissionAlerts([])

        assert a != permissions
        assert hash(a) != hash(permissions)
        assert a is not permissions
