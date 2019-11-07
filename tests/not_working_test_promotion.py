import pytest

from yandex_music import Promotion


@pytest.fixture(scope='class')
def promotion():
    return Promotion(TestPromotion.promo_id, TestPromotion.title, TestPromotion.subtitle, TestPromotion.heading,
                     TestPromotion.url, TestPromotion.url_scheme, TestPromotion.text_color, TestPromotion.gradient,
                     TestPromotion.image)


class TestPromotion:
    promo_id = None
    title = None
    subtitle = None
    heading = None
    url = None
    url_scheme = None
    text_color = None
    gradient = None
    image = None

    def test_expected_values(self, promotion):
        assert promotion.promo_id == self.promo_id
        assert promotion.title == self.title
        assert promotion.subtitle == self.subtitle
        assert promotion.heading == self.heading
        assert promotion.url == self.url
        assert promotion.url_scheme == self.url_scheme
        assert promotion.text_color == self.text_color
        assert promotion.gradient == self.gradient
        assert promotion.image == self.image

    def test_de_json_required(self, client):
        json_dict = {'promo_id': self.promo_id, 'title': self.title, 'subtitle': self.subtitle, 'heading': self.heading,
                     'url': self.url, 'url_scheme': self.url_scheme, 'text_color': self.text_color,
                     'gradient': self.gradient, 'image': self.image}
        promotion = Promotion.de_json(json_dict, client)

        assert promotion.promo_id == self.promo_id
        assert promotion.title == self.title
        assert promotion.subtitle == self.subtitle
        assert promotion.heading == self.heading
        assert promotion.url == self.url
        assert promotion.url_scheme == self.url_scheme
        assert promotion.text_color == self.text_color
        assert promotion.gradient == self.gradient
        assert promotion.image == self.image

    def test_de_json_all(self, client):
        json_dict = {'promo_id': self.promo_id, 'title': self.title, 'subtitle': self.subtitle, 'heading': self.heading,
                     'url': self.url, 'url_scheme': self.url_scheme, 'text_color': self.text_color,
                     'gradient': self.gradient, 'image': self.image}
        promotion = Promotion.de_json(json_dict, client)

        assert promotion.promo_id == self.promo_id
        assert promotion.title == self.title
        assert promotion.subtitle == self.subtitle
        assert promotion.heading == self.heading
        assert promotion.url == self.url
        assert promotion.url_scheme == self.url_scheme
        assert promotion.text_color == self.text_color
        assert promotion.gradient == self.gradient
        assert promotion.image == self.image

    def test_equality(self):
        pass
