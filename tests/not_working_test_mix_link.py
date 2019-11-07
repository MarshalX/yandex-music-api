import pytest

from yandex_music import MixLink


@pytest.fixture(scope='class')
def mix_link():
    return MixLink(TestMixLink.title, TestMixLink.url, TestMixLink.url_scheme, TestMixLink.text_color,
                   TestMixLink.background_color, TestMixLink.background_image_uri, TestMixLink.cover_white)


class TestMixLink:
    title = None
    url = None
    url_scheme = None
    text_color = None
    background_color = None
    background_image_uri = None
    cover_white = None

    def test_expected_values(self, mix_link):
        assert mix_link.title == self.title
        assert mix_link.url == self.url
        assert mix_link.url_scheme == self.url_scheme
        assert mix_link.text_color == self.text_color
        assert mix_link.background_color == self.background_color
        assert mix_link.background_image_uri == self.background_image_uri
        assert mix_link.cover_white == self.cover_white

    def test_de_json_required(self, client):
        json_dict = {'title': self.title, 'url': self.url, 'url_scheme': self.url_scheme, 'text_color': self.text_color,
                     'background_color': self.background_color, 'background_image_uri': self.background_image_uri,
                     'cover_white': self.cover_white}
        mix_link = MixLink.de_json(json_dict, client)

        assert mix_link.title == self.title
        assert mix_link.url == self.url
        assert mix_link.url_scheme == self.url_scheme
        assert mix_link.text_color == self.text_color
        assert mix_link.background_color == self.background_color
        assert mix_link.background_image_uri == self.background_image_uri
        assert mix_link.cover_white == self.cover_white

    def test_de_json_all(self, client):
        json_dict = {'title': self.title, 'url': self.url, 'url_scheme': self.url_scheme, 'text_color': self.text_color,
                     'background_color': self.background_color, 'background_image_uri': self.background_image_uri,
                     'cover_white': self.cover_white}
        mix_link = MixLink.de_json(json_dict, client)

        assert mix_link.title == self.title
        assert mix_link.url == self.url
        assert mix_link.url_scheme == self.url_scheme
        assert mix_link.text_color == self.text_color
        assert mix_link.background_color == self.background_color
        assert mix_link.background_image_uri == self.background_image_uri
        assert mix_link.cover_white == self.cover_white

    def test_equality(self):
        pass
