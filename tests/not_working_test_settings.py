from yandex_music import Settings


class TestSettings:
    web_payment_url = None
    promo_codes_enabled = None
    web_payment_month_product_price = None

    def test_expected_values(self, settings, in_app_products, native_products):
        assert settings.in_app_products == in_app_products
        assert settings.native_products == native_products
        assert settings.web_payment_url == self.web_payment_url
        assert settings.promo_codes_enabled == self.promo_codes_enabled
        assert settings.web_payment_month_product_price == self.web_payment_month_product_price

    def test_de_json_required(self, client, in_app_products, native_products):
        json_dict = {'in_app_products': in_app_products, 'native_products': native_products,
                     'web_payment_url': self.web_payment_url, 'promo_codes_enabled': self.promo_codes_enabled}
        settings = Settings.de_json(json_dict, client)

        assert settings.in_app_products == in_app_products
        assert settings.native_products == native_products
        assert settings.web_payment_url == self.web_payment_url
        assert settings.promo_codes_enabled == self.promo_codes_enabled

    def test_de_json_all(self, client, in_app_products, native_products):
        json_dict = {'in_app_products': in_app_products, 'native_products': native_products,
                     'web_payment_url': self.web_payment_url, 'promo_codes_enabled': self.promo_codes_enabled,
                     'web_payment_month_product_price': self.web_payment_month_product_price}
        settings = Settings.de_json(json_dict, client)

        assert settings.in_app_products == in_app_products
        assert settings.native_products == native_products
        assert settings.web_payment_url == self.web_payment_url
        assert settings.promo_codes_enabled == self.promo_codes_enabled
        assert settings.web_payment_month_product_price == self.web_payment_month_product_price

    def test_equality(self):
        pass
