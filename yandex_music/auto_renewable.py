from datetime import datetime

from yandex_music import YandexMusicObject, Product


class AutoRenewable(YandexMusicObject):
    def __init__(self,
                 expires,
                 vendor,
                 vendor_help_url,
                 product_id,
                 product,
                 order_id,
                 finished,
                 client=None,
                 **kwargs):
        self.expires = datetime.fromisoformat(expires)
        self.vendor = vendor
        self.vendor_help_url = vendor_help_url
        self.product_id = product_id
        self.product = product
        self.order_id = int(order_id)
        self.finished = bool(finished)

        self.client = client
        self._id_attrs = (self.order_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(AutoRenewable, cls).de_json(data, client)
        data['product'] = Product.de_json(data['product'], client=client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        auto_renewables = list()
        for auto_renewable in data:
            auto_renewables.append(cls.de_json(auto_renewable, client))

        return auto_renewables
