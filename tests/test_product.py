from yandex_music import Product


class TestProduct:
    product_id = 'ru.yandex.mobile.music.1month.autorenewable.native.web.notrial.restricted.cache.99'
    type = 'subscription'
    common_period_duration = 'P1M'
    description = None
    duration = 30
    trial_duration = 0
    feature = 'basic-music'
    debug = False
    features = ['basic-music']
    available = None
    trial_available = None
    vendor_trial_available = None
    button_text = None
    button_additional_text = None
    payment_method_types = None

    def test_expected_values(self, product, price):
        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.common_period_duration == self.common_period_duration
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug
        assert product.features == self.features
        assert product.description == self.description
        assert product.available == self.available
        assert product.trial_available == self.trial_available
        assert product.vendor_trial_available == self.vendor_trial_available
        assert product.button_text == self.button_text
        assert product.button_additional_text == self.button_additional_text
        assert product.payment_method_types == self.payment_method_types

    def test_de_json_none(self, client):
        assert Product.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Product.de_list({}, client) == []

    def test_de_json_required(self, client, price):
        json_dict = {'product_id': self.product_id, 'type_': self.type,
                     'common_period_duration': self.common_period_duration, 'duration': self.duration,
                     'trial_duration': self.trial_duration, 'price': price.to_dict(), 'feature': self.feature,
                     'debug': self.debug}
        product = Product.de_json(json_dict, client)

        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.common_period_duration == self.common_period_duration
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug

    def test_de_json_all(self, client, price):
        json_dict = {'product_id': self.product_id, 'type_': self.type,
                     'common_period_duration': self.common_period_duration, 'duration': self.duration,
                     'trial_duration': self.trial_duration, 'price': price.to_dict(), 'feature': self.feature,
                     'debug': self.debug, 'features': self.features, 'description': self.description,
                     'available': self.available, 'trial_available': self.trial_available,
                     'vendor_trial_available': self.vendor_trial_available, 'button_text': self.button_text,
                     'button_additional_text': self.button_additional_text,
                     'payment_method_types': self.payment_method_types}
        product = Product.de_json(json_dict, client)

        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.common_period_duration == self.common_period_duration
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug
        assert product.features == self.features
        assert product.description == self.description
        assert product.available == self.available
        assert product.trial_available == self.trial_available
        assert product.vendor_trial_available == self.vendor_trial_available
        assert product.button_text == self.button_text
        assert product.button_additional_text == self.button_additional_text
        assert product.payment_method_types == self.payment_method_types

    def test_equality(self, price):
        a = Product(self.product_id, self.type, self.common_period_duration, self.duration, self.trial_duration, price,
                    self.feature, self.debug)
        b = Product('', self.type, self.common_period_duration, self.duration, self.trial_duration, price,
                    self.feature, self.debug)
        c = Product(self.product_id, self.type, self.common_period_duration, self.duration, self.trial_duration, price,
                    self.feature, self.debug)

        assert a != b
        assert hash(a) != hash(b)

        assert a == c
