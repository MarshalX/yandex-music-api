from yandex_music import YandexMusicObject, Price


class Product(YandexMusicObject):
    def __init__(self,
                 product_id,
                 type,
                 common_period_duration,
                 duration,
                 trial_duration,
                 price,
                 feature,
                 debug,
                 client=None,
                 **kwargs):
        self.product_id = product_id
        self.type = type
        self.common_period_duration = common_period_duration
        self.duration = int(duration)
        self.trial_duration = int(trial_duration)
        self.price = price
        self.feature = feature
        self.debug = bool(debug)

        self.client = client
        self._id_attrs = (self.product_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Product, cls).de_json(data, client)
        data['price'] = Price.de_json(data['price'], client=client)

        return cls(client=client, **data)
