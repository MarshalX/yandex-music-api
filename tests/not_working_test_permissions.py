from yandex_music import Permissions


class TestPermissions:
    until = None
    values = None
    default = None

    def test_expected_values(self, permissions):
        assert permissions.until == self.until
        assert permissions.values == self.values
        assert permissions.default == self.default

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
        pass
