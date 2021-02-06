from yandex_music import MixLink


class TestMixLink:
    title = 'Беларусь'
    url = '/tag/belarus'
    url_scheme = 'yandexmusic://tag/belarus'
    text_color = '#6c65a9'
    background_color = 'transparent'
    background_image_uri = (
        'avatars.yandex.net/get-music-misc/28592/mix.5cf0bd5e58ea3a1e70caa07b.' 'background-image.1559281047248/%%'
    )
    cover_white = 'avatars.yandex.net/get-music-misc/28052/mix.5cf0bd5e58ea3a1e70caa07b.cover-white.1559281049219/%%'
    cover_uri = 'avatars.yandex.net/get-music-misc/34161/mix.57c6d15a2d3213a86ac653d2.cover.1555818786846/%%'

    def test_expected_values(self, mix_link):
        assert mix_link.title == self.title
        assert mix_link.url == self.url
        assert mix_link.url_scheme == self.url_scheme
        assert mix_link.text_color == self.text_color
        assert mix_link.background_color == self.background_color
        assert mix_link.background_image_uri == self.background_image_uri
        assert mix_link.cover_white == self.cover_white
        assert mix_link.cover_uri == self.cover_uri

    def test_de_json_none(self, client):
        assert MixLink.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert MixLink.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {
            'title': self.title,
            'url': self.url,
            'url_scheme': self.url_scheme,
            'text_color': self.text_color,
            'background_color': self.background_color,
            'background_image_uri': self.background_image_uri,
            'cover_white': self.cover_white,
        }
        mix_link = MixLink.de_json(json_dict, client)

        assert mix_link.title == self.title
        assert mix_link.url == self.url
        assert mix_link.url_scheme == self.url_scheme
        assert mix_link.text_color == self.text_color
        assert mix_link.background_color == self.background_color
        assert mix_link.background_image_uri == self.background_image_uri
        assert mix_link.cover_white == self.cover_white

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'url': self.url,
            'url_scheme': self.url_scheme,
            'text_color': self.text_color,
            'background_color': self.background_color,
            'background_image_uri': self.background_image_uri,
            'cover_white': self.cover_white,
            'cover_uri': self.cover_uri,
        }
        mix_link = MixLink.de_json(json_dict, client)

        assert mix_link.title == self.title
        assert mix_link.url == self.url
        assert mix_link.url_scheme == self.url_scheme
        assert mix_link.text_color == self.text_color
        assert mix_link.background_color == self.background_color
        assert mix_link.background_image_uri == self.background_image_uri
        assert mix_link.cover_white == self.cover_white
        assert mix_link.cover_uri == self.cover_uri

    def test_equality(self):
        a = MixLink(
            self.title,
            self.url,
            self.url_scheme,
            self.text_color,
            self.background_color,
            self.background_image_uri,
            self.cover_white,
        )
        b = MixLink(
            self.title,
            self.url,
            '',
            self.text_color,
            self.background_color,
            self.background_image_uri,
            self.cover_white,
        )
        c = MixLink(
            self.title,
            self.url,
            self.url_scheme,
            '#000000',
            self.background_color,
            self.background_image_uri,
            self.cover_white,
        )
        d = MixLink(
            self.title,
            self.url,
            self.url_scheme,
            self.text_color,
            self.background_color,
            self.background_image_uri,
            self.cover_white,
        )

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
