from yandex_music import Major


class TestMajor:
    id = 4
    name = 'WARNER'

    def test_expected_values(self, major):
        assert major.id == self.id
        assert major.name == self.name

    def test_de_json_none(self, client):
        assert Major.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'id': self.id, 'name': self.name}
        major = Major.de_json(json_dict, client)

        assert major.id == self.id
        assert major.name == self.name

    def test_de_json_all(self, client):
        json_dict = {'id': self.id, 'name': self.name}
        major = Major.de_json(json_dict, client)

        assert major.id == self.id
        assert major.name == self.name

    def test_equality(self):
        a = Major(self.id, self.name)
        b = Major(10, self.name)
        c = Major(self.id, self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
