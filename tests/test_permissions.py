from yandex_music import Permissions


class TestPermissions:
    until = '2019-11-07T23:53:55+00:00'
    values = ['landing-play', 'feed-play', 'mix-play']
    default = ['landing-play', 'feed-play', 'mix-play']

    def test_expected_values(self, permissions):
        assert permissions.until == self.until
        assert permissions.values == self.values
        assert permissions.default == self.default

    def test_de_json_none(self, client):
        assert Permissions.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'until': self.until, 'values': self.values, 'default': self.default}
        permissions = Permissions.de_json(json_dict, client)

        assert permissions.until == self.until
        assert permissions.values == self.values
        assert permissions.default == self.default

    def test_de_json_all(self, client):
        json_dict = {'until': self.until, 'values': self.values, 'default': self.default}
        permissions = Permissions.de_json(json_dict, client)

        assert permissions.until == self.until
        assert permissions.values == self.values
        assert permissions.default == self.default

    def test_equality(self):
        a = Permissions(self.until, self.values, self.default)
        b = Permissions('', self.values, self.default)
        c = Permissions(self.until, self.values, self.default)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
