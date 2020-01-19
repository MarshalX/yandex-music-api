from yandex_music import Vinyl


class TestVinyl:
    url = 'http://www.ozon.ru/context/detail/id/29504873/?partner=yandexmusic'
    picture = 'avatars.yandex.net/get-music-misc/2413828/vinyl.29504873image/%%'
    title = 'The Prodigy.Their Law The Singles 1990-2005 (2 LP)'
    year = 2005
    media = '2 Грампластинка (LP)'
    price = 4483

    def test_expected_values(self, vinyl):
        assert vinyl.url == self.url
        assert vinyl.picture == self.picture
        assert vinyl.title == self.title
        assert vinyl.year == self.year
        assert vinyl.price == self.price
        assert vinyl.media == self.media

    def test_de_json_none(self, client):
        assert Vinyl.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Vinyl.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'url': self.url, 'title': self.title, 'year': self.year, 'price': self.price, 'media': self.media}
        vinyl = Vinyl.de_json(json_dict, client)

        assert vinyl.url == self.url
        assert vinyl.title == self.title
        assert vinyl.year == self.year
        assert vinyl.price == self.price
        assert vinyl.media == self.media

    def test_de_json_all(self, client):
        json_dict = {'url': self.url, 'picture': self.picture, 'title': self.title, 'year': self.year,
                     'price': self.price, 'media': self.media}
        vinyl = Vinyl.de_json(json_dict, client)

        assert vinyl.url == self.url
        assert vinyl.picture == self.picture
        assert vinyl.title == self.title
        assert vinyl.year == self.year
        assert vinyl.price == self.price
        assert vinyl.media == self.media

    def test_equality(self):
        a = Vinyl(self.url, self.title, 2020, 200, self.media, self.picture)
        b = Vinyl(self.url, self.title, self.year, self.price, self.media, self.picture)
        c = Vinyl(self.url, self.title, self.year, self.price, self.media, self.picture)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert b == c
