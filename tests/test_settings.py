from yandex_music import Settings


class TestSettings:
    web_payment_url = 'https://music.yandex.ru/webview/payment'
    promo_codes_enabled = True

    def test_expected_values(self, settings, product, price):
        assert settings.in_app_products == [product]
        assert settings.native_products == [product]
        assert settings.web_payment_url == self.web_payment_url
        assert settings.promo_codes_enabled == self.promo_codes_enabled
        assert settings.web_payment_month_product_price == price

    def test_de_json_none(self, client):
        assert Settings.de_json({}, client) is None

    def test_de_json_required(self, client, product):
        json_dict = {
            'in_app_products': [product.to_dict()],
            'native_products': [product.to_dict()],
            'web_payment_url': self.web_payment_url,
            'promo_codes_enabled': self.promo_codes_enabled,
        }
        settings = Settings.de_json(json_dict, client)

        assert settings.in_app_products == [product]
        assert settings.native_products == [product]
        assert settings.web_payment_url == self.web_payment_url
        assert settings.promo_codes_enabled == self.promo_codes_enabled

    def test_de_json_all(self, client, product, price):
        json_dict = {
            'in_app_products': [product.to_dict()],
            'native_products': [product.to_dict()],
            'web_payment_url': self.web_payment_url,
            'promo_codes_enabled': self.promo_codes_enabled,
            'web_payment_month_product_price': price.to_dict(),
        }
        settings = Settings.de_json(json_dict, client)

        assert settings.in_app_products == [product]
        assert settings.native_products == [product]
        assert settings.web_payment_url == self.web_payment_url
        assert settings.promo_codes_enabled == self.promo_codes_enabled
        assert settings.web_payment_month_product_price == price

    def test_equality(self, product):
        a = Settings([product], [product], self.web_payment_url, self.promo_codes_enabled)
        b = Settings([product], [product], '', self.promo_codes_enabled)
        c = Settings([product], [product], self.web_payment_url, False)
        d = Settings([product], [product], self.web_payment_url, self.promo_codes_enabled)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
