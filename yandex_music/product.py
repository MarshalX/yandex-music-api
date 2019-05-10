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
                 features=None,
                 description=None,
                 available=None,
                 trial_available=None,
                 vendor_trial_available=None,
                 button_text=None,
                 button_additional_text=None,
                 payment_method_types=None,
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

        self.features = features
        self.description = description
        self.available = available
        self.trial_available = trial_available
        self.vendor_trial_available = vendor_trial_available
        self.button_text = button_text
        self.button_additional_text = button_additional_text
        self.payment_method_types = payment_method_types

        self.client = client
        self._id_attrs = (self.product_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Product, cls).de_json(data, client)
        data['price'] = Price.de_json(data.get('price'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        products = list()
        for product in data:
            products.append(cls.de_json(product, client))

        return products
