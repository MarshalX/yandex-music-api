from typing import Dict, Optional

from yandex_music import Account, Alert, Client, JSONType, Permissions, Plus, Status, Subscription


class TestStatus:
    advertisement = 'Оформите постоянную подписку – первый месяц бесплатно!'
    cache_limit = 99
    subeditor = False
    subeditor_level = 0
    default_email = 'yandex_music@yandex.com'
    skips_per_hour: Optional[int] = None
    station_exists: Optional[bool] = None
    premium_region: Optional[int] = None
    experiment = 109
    pretrial_active = False
    userhash = '2a1d970ce4dadc3333280aa8727d1c41a380a7622521ecef67928cd4213adb8f'
    has_options = ['bookmate']

    def test_expected_values(
        self,
        status: Status,
        account: Account,
        permissions: Permissions,
        subscription: Subscription,
        plus: Plus,
        alert: Alert,
    ) -> None:
        assert status.account == account
        assert status.permissions == permissions
        assert status.subscription == subscription
        assert status.advertisement == self.advertisement
        assert status.cache_limit == self.cache_limit
        assert status.subeditor == self.subeditor
        assert status.subeditor_level == self.subeditor_level
        assert status.plus == plus
        assert status.default_email == self.default_email
        assert status.skips_per_hour == self.skips_per_hour
        assert status.station_exists == self.station_exists
        assert status.bar_below == alert
        assert status.premium_region == self.premium_region
        assert status.experiment == self.experiment
        assert status.pretrial_active == self.pretrial_active
        assert status.userhash == self.userhash
        assert status.has_options == self.has_options

    def test_de_json_none(self, client: Client) -> None:
        assert Status.de_json({}, client) is None

    def test_de_json_required(self, client: Client, account: Account, permissions: Permissions) -> None:
        json_dict: Dict[str, JSONType] = {'account': account.to_dict(), 'permissions': permissions.to_dict()}
        status = Status.de_json(json_dict, client)
        assert status is not None

        assert status.account == account
        assert status.permissions == permissions

    def test_de_json_all(
        self,
        client: Client,
        account: Account,
        permissions: Permissions,
        subscription: Subscription,
        plus: Plus,
        alert: Alert,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'account': account.to_dict(),
            'permissions': permissions.to_dict(),
            'subscription': subscription.to_dict(),
            'cache_limit': self.cache_limit,
            'subeditor': self.subeditor,
            'subeditor_level': self.subeditor_level,
            'plus': plus.to_dict(),
            'default_email': self.default_email,
            'skips_per_hour': self.skips_per_hour,
            'station_exists': self.station_exists,
            'premium_region': self.premium_region,
            'advertisement': self.advertisement,
            'bar_below': alert.to_dict(),
            'experiment': self.experiment,
            'pretrial_active': self.pretrial_active,
            'userhash': self.userhash,
            'hasOptions': self.has_options,
        }
        status = Status.de_json(json_dict, client)
        assert status is not None

        assert status.account == account
        assert status.permissions == permissions
        assert status.subscription == subscription
        assert status.advertisement == self.advertisement
        assert status.cache_limit == self.cache_limit
        assert status.subeditor == self.subeditor
        assert status.subeditor_level == self.subeditor_level
        assert status.plus == plus
        assert status.default_email == self.default_email
        assert status.skips_per_hour == self.skips_per_hour
        assert status.station_exists == self.station_exists
        assert status.bar_below == alert
        assert status.premium_region == self.premium_region
        assert status.experiment == self.experiment
        assert status.pretrial_active == self.pretrial_active
        assert status.userhash == self.userhash
        assert status.has_options == self.has_options

    def test_equality(self, account: Account, permissions: Permissions, subscription: Subscription) -> None:
        a = Status(account, permissions)
        b = Status(None, permissions)
        c = Status(account, permissions)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
