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
        self.cache_limit = cache_limit
        self.subscription = subscription
        self.subeditor = subeditor
        self.subeditor_level = subeditor_level
        self.plus = plus
        self.default_email = default_email

        self.client = client
        self._id_attrs = (self.account,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Status, cls).de_json(data, client)
        data['account'] = Account.de_json(data.get('account'), client)
        data['permissions'] = Permissions.de_json(data.get('permissions'), client)
        data['subscription'] = Subscription.de_json(data.get('subscription'), client)
        data['plus'] = Plus.de_json(data.get('plus'), client)

        return cls(client=client, **data)
