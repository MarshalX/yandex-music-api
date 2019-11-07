import pytest

from yandex_music import Status


@pytest.fixture(scope='class')
def status(account, permissions, subscription, plus):
    return Status(account, permissions, subscription, TestStatus.cache_limit, TestStatus.subeditor,
                  TestStatus.subeditor_level, plus, TestStatus.default_email, TestStatus.skips_per_hour,
                  TestStatus.station_exists, TestStatus.premium_region)


class TestStatus:
    cache_limit = None
    subeditor = None
    subeditor_level = None
    default_email = None
    skips_per_hour = None
    station_exists = None
    premium_region = None

    def test_expected_values(self, status, account, permissions, subscription, plus):
        assert status.account == account
        assert status.permissions == permissions
        assert status.subscription == subscription
        assert status.cache_limit == self.cache_limit
        assert status.subeditor == self.subeditor
        assert status.subeditor_level == self.subeditor_level
        assert status.plus == plus
        assert status.default_email == self.default_email
        assert status.skips_per_hour == self.skips_per_hour
        assert status.station_exists == self.station_exists
        assert status.premium_region == self.premium_region

    def test_de_json_required(self, client, account, permissions):
        json_dict = {'account': account, 'permissions': permissions}
        status = Status.de_json(json_dict, client)

        assert status.account == account
        assert status.permissions == permissions

    def test_de_json_all(self, client, account, permissions, subscription, plus):
        json_dict = {'account': account, 'permissions': permissions, 'subscription': subscription,
                     'cache_limit': self.cache_limit, 'subeditor': self.subeditor,
                     'subeditor_level': self.subeditor_level, 'plus': plus, 'default_email': self.default_email,
                     'skips_per_hour': self.skips_per_hour, 'station_exists': self.station_exists,
                     'premium_region': self.premium_region}
        status = Status.de_json(json_dict, client)

        assert status.account == account
        assert status.permissions == permissions
        assert status.subscription == subscription
        assert status.cache_limit == self.cache_limit
        assert status.subeditor == self.subeditor
        assert status.subeditor_level == self.subeditor_level
        assert status.plus == plus
        assert status.default_email == self.default_email
        assert status.skips_per_hour == self.skips_per_hour
        assert status.station_exists == self.station_exists
        assert status.premium_region == self.premium_region

    def test_equality(self):
        pass
