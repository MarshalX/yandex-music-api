from yandex_music import Promotion


class TestPromotion:
    promo_id = '5db861cfa6245a2c8c63445d'
    title = '«Никакого андеграунда!»'
    subtitle = 'на новой пластинке группы «Папин Олимпос»'
    heading = 'Мини-альбом'
    url = '/album/8839440'
    url_scheme = 'yandexmusic://album/8839440'
    text_color = ''
    gradient = ''
    image = 'avatars.yandex.net/get-music-feed-promotion/69892/5db861cfa6245a2c8c63445d-landing.image/%%'

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

    def test_de_list_none(self, client):
        assert Promotion.de_list({}, client) == []

    def test_de_json_none(self, client):
        assert Promotion.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'promo_id': self.promo_id,
            'title': self.title,
            'subtitle': self.subtitle,
            'heading': self.heading,
            'url': self.url,
            'url_scheme': self.url_scheme,
            'text_color': self.text_color,
            'gradient': self.gradient,
            'image': self.image,
        }
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
        json_dict = {
            'promo_id': self.promo_id,
            'title': self.title,
            'subtitle': self.subtitle,
            'heading': self.heading,
            'url': self.url,
            'url_scheme': self.url_scheme,
            'text_color': self.text_color,
            'gradient': self.gradient,
            'image': self.image,
        }
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
        a = Promotion(
            self.promo_id,
            self.title,
            self.subtitle,
            self.heading,
            self.url,
            self.url_scheme,
            self.text_color,
            self.gradient,
            self.image,
        )
        b = Promotion(
            '', self.title, self.subtitle, '', self.url, self.url_scheme, self.text_color, self.gradient, self.image
        )
        c = Promotion(
            self.promo_id,
            '',
            self.subtitle,
            self.heading,
            self.url,
            self.url_scheme,
            self.text_color,
            self.gradient,
            '',
        )
        d = Promotion(
            self.promo_id,
            self.title,
            self.subtitle,
            self.heading,
            self.url,
            self.url_scheme,
            self.text_color,
            self.gradient,
            self.image,
        )

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
