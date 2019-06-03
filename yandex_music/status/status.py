from yandex_music import YandexMusicObject


class Status(YandexMusicObject):
    def __init__(self,
                 account,
                 permissions,
                 subscription,
                 cache_limit=None,
                 subeditor=None,
                 subeditor_level=None,
                 plus=None,
                 default_email=None,
                 skips_per_hour=None,
                 station_exists=None,
                 premium_region=None,
                 client=None,
                 **kwargs):
        self.account = account
        self.permissions = permissions
        self.subscription = subscription

        self.cache_limit = cache_limit
        self.subeditor = subeditor
        self.subeditor_level = subeditor_level
        self.plus = plus
        self.default_email = default_email
        self.skips_per_hour = skips_per_hour
        self.station_exists = station_exists
        self.premium_region = premium_region

        self.client = client
        self._id_attrs = (self.account,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Status, cls).de_json(data, client)
        from yandex_music import Account, Permissions, Plus, Subscription
        data['account'] = Account.de_json(data.get('account'), client)
        data['permissions'] = Permissions.de_json(data.get('permissions'), client)
        data['subscription'] = Subscription.de_json(data.get('subscription'), client)
        data['plus'] = Plus.de_json(data.get('plus'), client)

        return cls(client=client, **data)
