from yandex_music import Status


class TestStatus:
    advertisement = 'Оформите постоянную подписку – первый месяц бесплатно!'
    cache_limit = 99
    subeditor = False
    subeditor_level = 0
    default_email = 'Ilya@marshal.by'
    skips_per_hour = None
    station_exists = None
    premium_region = None
    experiment = 109

    def test_expected_values(self, status, account, permissions, subscription, plus, alert):
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

    def test_de_json_none(self, client):
        assert Status.de_json({}, client) is None

    def test_de_json_required(self, client, account, permissions):
        json_dict = {'account': account.to_dict(), 'permissions': permissions.to_dict()}
        status = Status.de_json(json_dict, client)

        assert status.account == account
        assert status.permissions == permissions

    def test_de_json_all(self, client, account, permissions, subscription, plus, alert):
        json_dict = {
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
        }
        status = Status.de_json(json_dict, client)

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

    def test_equality(self, account, permissions, subscription):
        a = Status(account, permissions)
        b = Status(None, permissions)
        c = Status(account, permissions)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
