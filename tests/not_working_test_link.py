import pytest

from yandex_music import Link


@pytest.fixture(scope='class')
def link():
    return Link(TestLink.title, TestLink.href, TestLink.type, TestLink.social_network)


class TestLink:
    title = None
    href = None
    type = None
    social_network = None

    def test_expected_values(self, link):
        assert link.title == self.title
        assert link.href == self.href
        assert link.type == self.type
        assert link.social_network == self.social_network

    def test_de_json_required(self, client):
        json_dict = {'title': self.title, 'href': self.href, 'type': self.type}
        link = Link.de_json(json_dict, client)

        assert link.title == self.title
        assert link.href == self.href
        assert link.type == self.type

    def test_de_json_all(self, client):
        json_dict = {'title': self.title, 'href': self.href, 'type': self.type, 'social_network': self.social_network}
        link = Link.de_json(json_dict, client)

        assert link.title == self.title
        assert link.href == self.href
        assert link.type == self.type
        assert link.social_network == self.social_network

    def test_equality(self):
        pass
