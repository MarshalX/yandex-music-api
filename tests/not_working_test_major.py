from yandex_music import Major


class TestMajor:
    name = None

    def test_expected_values(self, major, id):
        assert major.id == id
        assert major.name == self.name

    def test_de_json_required(self, client, id):
        json_dict = {'id': id, 'name': self.name}
        major = Major.de_json(json_dict, client)

        assert major.id == id
        assert major.name == self.name

    def test_de_json_all(self, client, id):
        json_dict = {'id': id, 'name': self.name}
        major = Major.de_json(json_dict, client)

        assert major.id == id
        assert major.name == self.name

    def test_equality(self):
        pass
