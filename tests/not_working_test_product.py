from yandex_music import Product


class TestProduct:
    product_id = None
    type = None
    common_period_duration = None
    duration = None
    trial_duration = None
    feature = None
    debug = None
    features = None
    available = None
    trial_available = None
    vendor_trial_available = None
    button_text = None
    button_additional_text = None
    payment_method_types = None

    def test_expected_values(self, product, price, description):
        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.common_period_duration == self.common_period_duration
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug
        assert product.features == self.features
        assert product.description == description
        assert product.available == self.available
        assert product.trial_available == self.trial_available
        assert product.vendor_trial_available == self.vendor_trial_available
        assert product.button_text == self.button_text
        assert product.button_additional_text == self.button_additional_text
        assert product.payment_method_types == self.payment_method_types

    def test_de_json_required(self, client, price):
        json_dict = {'product_id': self.product_id, 'type': self.type,
                     'common_period_duration': self.common_period_duration, 'duration': self.duration,
                     'trial_duration': self.trial_duration, 'price': price, 'feature': self.feature,
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

    def test_de_json_all(self, client, price, description):
        json_dict = {'product_id': self.product_id, 'type': self.type,
                     'common_period_duration': self.common_period_duration, 'duration': self.duration,
                     'trial_duration': self.trial_duration, 'price': price, 'feature': self.feature,
                     'debug': self.debug, 'features': self.features, 'description': description,
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
        assert product.description == description
        assert product.available == self.available
        assert product.trial_available == self.trial_available
        assert product.vendor_trial_available == self.vendor_trial_available
        assert product.button_text == self.button_text
        assert product.button_additional_text == self.button_additional_text
        assert product.payment_method_types == self.payment_method_types

    def test_equality(self):
        pass
