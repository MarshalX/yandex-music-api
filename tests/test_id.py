from yandex_music import Id


class TestId:
    type = 'user'
    tag = 'onyourwave'

    def test_expected_values(self, id_):
        assert id_.type == self.type
        assert id_.tag == self.tag

    def test_de_json_none(self, client):
        assert Id.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'type': self.type, 'tag': self.tag}
        id_ = Id.de_json(json_dict, client)

        assert id_.type == self.type
        assert id_.tag == self.tag

    def test_de_json_all(self, client):
        json_dict = {'type': self.type, 'tag': self.tag}
        id_ = Id.de_json(json_dict, client)

        assert id_.type == self.type
        assert id_.tag == self.tag

    def test_equality(self):
        a = Id(self.type, self.tag)
        b = Id('', self.tag)
        c = Id(self.type, '')
        d = Id(self.type, self.tag)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
