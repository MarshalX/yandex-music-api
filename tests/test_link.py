from yandex_music import Link


class TestLink:
    title = 'emmure'
    href = 'https://www.facebook.com/emmure'
    type = 'social'
    social_network = 'facebook'

    def test_expected_values(self, link):
        assert link.title == self.title
        assert link.href == self.href
        assert link.type == self.type
        assert link.social_network == self.social_network

    def test_de_json_none(self, client):
        assert Link.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Link.de_list({}, client) == []

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
        a = Link(self.title, self.href, self.type, self.social_network)
        b = Link(self.title, '', self.type, self.social_network)
        c = Link(self.title, self.href, '', self.social_network)
        d = Link(self.title, self.href, self.type, self.social_network)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
