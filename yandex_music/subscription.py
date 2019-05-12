from yandex_music import YandexMusicObject


class Subscription(YandexMusicObject):
    def __init__(self,
                 auto_renewable,
                 can_start_trial,
                 mcdonalds,
                 client=None,
                 **kwargs):
        self.auto_renewable = auto_renewable
        self.can_start_trial = can_start_trial
        self.mcdonalds = mcdonalds

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Subscription, cls).de_json(data, client)
        from yandex_music import AutoRenewable
        data['auto_renewable'] = AutoRenewable.de_list(data.get('auto_renewable'), client)

        return cls(client=client, **data)
