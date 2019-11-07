from yandex_music import Id


class TestId:
    type = None
    tag = None

    def test_expected_values(self, id):
        assert id.type == self.type
        assert id.tag == self.tag

    def test_de_json_required(self, client):
        json_dict = {'type': self.type, 'tag': self.tag}
        id = Id.de_json(json_dict, client)

        assert id.type == self.type
        assert id.tag == self.tag

    def test_de_json_all(self, client):
        json_dict = {'type': self.type, 'tag': self.tag}
        id = Id.de_json(json_dict, client)

        assert id.type == self.type
        assert id.tag == self.tag

    def test_equality(self):
        pass
