from typing import Dict, List, Optional

from yandex_music import Client, JSONType, LicenceTextPart, Price, Product


class TestProduct:
    product_id = 'ru.yandex.mobile.music.1month.autorenewable.native.web.notrial.restricted.cache.99'
    type = 'subscription'
    common_period_duration = 'P1M'
    description: Optional[str] = None
    duration = 30
    trial_duration = 0
    feature = 'basic-music'
    debug = False
    plus = False
    cheapest = True
    title = 'КиноПоиск HD'
    family_sub = False
    fb_image = ''
    fb_name = 'kinopoisk-plus'
    family = False
    features = ['basic-music']
    available: Optional[bool] = None
    trial_available: Optional[bool] = None
    trial_period_duration = 'P1M'
    intro_period_duration = 'P1Y'
    start_period_duration = 'P1M'
    vendor_trial_available: Optional[bool] = None
    button_text: Optional[str] = None
    button_additional_text: Optional[str] = None
    payment_method_types: Optional[List[str]] = None

    def test_expected_values(self, product: Product, price: Price, licence_text_part: LicenceTextPart) -> None:
        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.common_period_duration == self.common_period_duration
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug
        assert product.plus == self.plus
        assert product.cheapest == self.cheapest
        assert product.title == self.title
        assert product.family_sub == self.family_sub
        assert product.fb_image == self.fb_image
        assert product.fb_name == self.fb_name
        assert product.family == self.family
        assert product.features == self.features
        assert product.description == self.description
        assert product.available == self.available
        assert product.trial_available == self.trial_available
        assert product.trial_period_duration == self.trial_period_duration
        assert product.intro_period_duration == self.intro_period_duration
        assert product.intro_price == price
        assert product.start_period_duration == self.start_period_duration
        assert product.start_price == price
        assert product.licence_text_parts == [licence_text_part]
        assert product.vendor_trial_available == self.vendor_trial_available
        assert product.button_text == self.button_text
        assert product.button_additional_text == self.button_additional_text
        assert product.payment_method_types == self.payment_method_types

    def test_de_json_none(self, client: Client) -> None:
        assert Product.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Product.de_list([], client) == []

    def test_de_json_required(self, client: Client, price: Price) -> None:
        json_dict: Dict[str, JSONType] = {
            'product_id': self.product_id,
            'type': self.type,
            'duration': self.duration,
            'trial_duration': self.trial_duration,
            'price': price.to_dict(),
            'feature': self.feature,
            'debug': self.debug,
            'plus': self.plus,
        }
        product = Product.de_json(json_dict, client)
        assert product is not None

        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug
        assert product.plus == self.plus

    def test_de_json_all(self, client: Client, price: Price, licence_text_part: LicenceTextPart) -> None:
        json_dict: Dict[str, JSONType] = {
            'product_id': self.product_id,
            'type': self.type,
            'common_period_duration': self.common_period_duration,
            'duration': self.duration,
            'trial_duration': self.trial_duration,
            'price': price.to_dict(),
            'feature': self.feature,
            'debug': self.debug,
            'plus': self.plus,
            'features': self.features,
            'description': self.description,
            'available': self.available,
            'trial_available': self.trial_available,
            'vendor_trial_available': self.vendor_trial_available,
            'button_text': self.button_text,
            'button_additional_text': self.button_additional_text,
            'cheapest': self.cheapest,
            'payment_method_types': self.payment_method_types,
            'title': self.title,
            'family': self.family,
            'family_sub': self.family_sub,
            'fb_image': self.fb_image,
            'fb_name': self.fb_name,
            'trial_period_duration': self.trial_period_duration,
            'intro_period_duration': self.intro_period_duration,
            'intro_price': price.to_dict(),
            'start_period_duration': self.start_period_duration,
            'start_price': price.to_dict(),
            'licence_text_parts': [licence_text_part.to_dict()],
        }
        product = Product.de_json(json_dict, client)
        assert product is not None

        assert product.product_id == self.product_id
        assert product.type == self.type
        assert product.common_period_duration == self.common_period_duration
        assert product.duration == self.duration
        assert product.trial_duration == self.trial_duration
        assert product.price == price
        assert product.feature == self.feature
        assert product.debug == self.debug
        assert product.plus == self.plus
        assert product.cheapest == self.cheapest
        assert product.title == self.title
        assert product.family_sub == self.family_sub
        assert product.fb_image == self.fb_image
        assert product.fb_name == self.fb_name
        assert product.family == self.family
        assert product.features == self.features
        assert product.description == self.description
        assert product.available == self.available
        assert product.trial_available == self.trial_available
        assert product.trial_period_duration == self.trial_period_duration
        assert product.intro_period_duration == self.intro_period_duration
        assert product.intro_price == price
        assert product.start_period_duration == self.start_period_duration
        assert product.start_price == price
        assert product.licence_text_parts == [licence_text_part]
        assert product.vendor_trial_available == self.vendor_trial_available
        assert product.button_text == self.button_text
        assert product.button_additional_text == self.button_additional_text
        assert product.payment_method_types == self.payment_method_types

    def test_equality(self, price: Price) -> None:
        a = Product(
            self.product_id,
            self.type,
            self.duration,
            self.trial_duration,
            self.feature,
            self.debug,
            self.plus,
            price,
        )
        b = Product(
            '',
            self.type,
            self.duration,
            self.trial_duration,
            self.feature,
            self.debug,
            self.plus,
            price,
        )
        c = Product(
            self.product_id,
            self.type,
            self.duration,
            self.trial_duration,
            self.feature,
            self.debug,
            self.plus,
            price,
        )

        assert a != b
        assert hash(a) != hash(b)

        assert a == c
