from yandex_music import Brand


class TestBrand:
    image = 'https://avatars.mds.yandex.net/get-music-misc/2419084/img.5dbb0478e482b01822a89af8/%%'
    background = '#2A2A2A'
    reference = 'yandexmusic://post/5c94a7bf433f8221feac3fa6'
    pixels = [
        'http://ads6.adfox.ru/256152/event?hash=84862c423eb&rand=eo=hdxqd&pr=deyq&p1=bwzel',
        'http://banners.adfox.ru/transparent.gif',
    ]
    theme = 'dark'
    playlist_theme = ''
    button = 'Больше подкастов'

    def test_expected_values(self, brand):
        assert brand.image == self.image
        assert brand.background == self.background
        assert brand.reference == self.reference
        assert brand.pixels == self.pixels
        assert brand.theme == self.theme
        assert brand.playlist_theme == self.playlist_theme
        assert brand.button == self.button

    def test_de_json_none(self, client):
        assert Brand.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'image': self.image,
            'background': self.background,
            'reference': self.reference,
            'pixels': self.pixels,
            'theme': self.theme,
            'playlist_theme': self.playlist_theme,
            'button': self.button,
        }
        brand = Brand.de_json(json_dict, client)

        assert brand.image == self.image
        assert brand.background == self.background
        assert brand.reference == self.reference
        assert brand.pixels == self.pixels
        assert brand.theme == self.theme
        assert brand.playlist_theme == self.playlist_theme
        assert brand.button == self.button

    def test_de_json_all(self, client):
        json_dict = {
            'image': self.image,
            'background': self.background,
            'reference': self.reference,
            'pixels': self.pixels,
            'theme': self.theme,
            'playlist_theme': self.playlist_theme,
            'button': self.button,
        }
        brand = Brand.de_json(json_dict, client)

        assert brand.image == self.image
        assert brand.background == self.background
        assert brand.reference == self.reference
        assert brand.pixels == self.pixels
        assert brand.theme == self.theme
        assert brand.playlist_theme == self.playlist_theme
        assert brand.button == self.button

    def test_equality(self):
        a = Brand(
            self.image, self.background, self.reference, self.pixels, self.theme, self.playlist_theme, self.button
        )
        b = Brand('', self.background, self.reference, ['link'], self.theme, self.playlist_theme, self.button)
        c = Brand(
            self.image, self.background, self.reference, self.pixels, self.theme, self.playlist_theme, self.button
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
