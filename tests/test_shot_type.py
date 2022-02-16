from yandex_music import ShotType


class TestShotType:
    id = 'alice'
    title = 'Шот от Алисы'

    def test_expected_values(self, shot_type):
        assert shot_type.id == self.id
        assert shot_type.title == self.title

    def test_de_json_none(self, client):
        assert ShotType.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'id': self.id, 'title': self.title}
        shot_type = ShotType.de_json(json_dict, client)

        assert shot_type.id == self.id
        assert shot_type.title == self.title

    def test_de_json_all(self, client):
        json_dict = {'id': self.id, 'title': self.title}
        shot_type = ShotType.de_json(json_dict, client)

        assert shot_type.id == self.id
        assert shot_type.title == self.title

    def test_equality(self):
        a = ShotType(self.id, self.title)
        b = ShotType('', self.title)
        c = ShotType(self.id, '')
        d = ShotType('', '')
        e = ShotType(self.id, self.title)

        assert a != b != c != d != e
        assert hash(a) != hash(b) != hash(c) != hash(d) != hash(e)
        assert a is not b is not c is not d is not e

        assert a == e
        assert hash(a) == hash(e)
