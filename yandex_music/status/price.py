from yandex_music import YandexMusicObject


class Price(YandexMusicObject):
    def __init__(self,
                 amount,
                 currency,
                 client=None,
                 **kwargs):
        self.amount = amount
        self.currency = currency

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Price, cls).de_json(data, client)

        return cls(client=client, **data)
