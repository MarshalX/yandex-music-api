from yandex_music import YandexMusicObject, Account, Permissions, Plus, Subscription


class Status(YandexMusicObject):
    def __init__(self,
                 account,
                 permissions,
                 cache_limit,
                 subscription,
                 subeditor,
                 subeditor_level,
                 plus,
                 default_email,
                 client=None,
                 **kwargs):
        self.account = account
        self.permissions = permissions
        self.cache_limit = int(cache_limit)
        self.subscription = subscription
        self.subeditor = bool(subeditor)
        self.subeditor_level = int(subeditor_level)
        self.plus = plus
        self.default_email = default_email

        self.client = client
        self._id_attrs = (self.account,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Status, cls).de_json(data, client)
        data['account'] = Account.de_json(data['account'], client=client)
        data['permissions'] = Permissions.de_json(data['permissions'], client=client)
        data['subscription'] = Subscription.de_json(data['subscription'], client=client)
        data['plus'] = Plus.de_json(data['plus'], client=client)

        return cls(client=client, **data)
