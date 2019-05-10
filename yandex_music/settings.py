from yandex_music import YandexMusicObject


class Settings(YandexMusicObject):
    def __init__(self,
                 in_app_products,
                 native_products,
                 web_payment_url,
                 promo_codes_enabled,
                 web_payment_month_product_price=None,
                 client=None,
                 **kwargs):
        self.in_app_products = in_app_products
        self.native_products = native_products
        self.web_payment_url = web_payment_url
        self.web_payment_month_product_price = web_payment_month_product_price
        self.promo_codes_enabled = bool(promo_codes_enabled)

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Settings, cls).de_json(data, client)
        from yandex_music import Product, Price
        data['in_app_products'] = Product.de_list(data.get('in_app_products'), client)
        data['native_products'] = Product.de_list(data.get('native_products'), client)
        data['web_payment_month_product_price'] = \
            Price.de_json(data.get('web_payment_month_product_price'), client)

        return cls(client=client, **data)
