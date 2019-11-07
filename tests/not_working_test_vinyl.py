import pytest

from yandex_music import Vinyl


@pytest.fixture(scope='class')
def vinyl():
    return Vinyl(TestVinyl.url, TestVinyl.picture, TestVinyl.title, TestVinyl.year, TestVinyl.price, TestVinyl.media)


class TestVinyl:
    url = None
    picture = None
    title = None
    year = None
    media = None

    def test_expected_values(self, vinyl, price):
        assert vinyl.url == self.url
        assert vinyl.picture == self.picture
        assert vinyl.title == self.title
        assert vinyl.year == self.year
        assert vinyl.price == price
        assert vinyl.media == self.media

    def test_de_json_required(self, client, price):
        json_dict = {'url': self.url, 'picture': self.picture, 'title': self.title, 'year': self.year, 'price': price,
                     'media': self.media}
        vinyl = Vinyl.de_json(json_dict, client)

        assert vinyl.url == self.url
        assert vinyl.picture == self.picture
        assert vinyl.title == self.title
        assert vinyl.year == self.year
        assert vinyl.price == price
        assert vinyl.media == self.media

    def test_de_json_all(self, client, price):
        json_dict = {'url': self.url, 'picture': self.picture, 'title': self.title, 'year': self.year, 'price': price,
                     'media': self.media}
        vinyl = Vinyl.de_json(json_dict, client)

        assert vinyl.url == self.url
        assert vinyl.picture == self.picture
        assert vinyl.title == self.title
        assert vinyl.year == self.year
        assert vinyl.price == price
        assert vinyl.media == self.media

    def test_equality(self):
        pass
