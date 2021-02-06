from yandex_music import Deprecation


class TestDeprecation:
    target_album_id = 11084011
    status = 'duplicate-of'
    done = True

    def test_expected_values(self, deprecation):
        assert deprecation.target_album_id == self.target_album_id
        assert deprecation.status == self.status
        assert deprecation.done == self.done

    def test_de_json_none(self, client):
        assert Deprecation.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'target_album_id': self.target_album_id, 'status': self.status, 'done': self.done}
        deprecation = Deprecation.de_json(json_dict, client)

        assert deprecation.target_album_id == self.target_album_id
        assert deprecation.status == self.status
        assert deprecation.done == self.done

    def test_de_json_all(self, client):
        json_dict = {'target_album_id': self.target_album_id, 'status': self.status, 'done': self.done}
        deprecation = Deprecation.de_json(json_dict, client)

        assert deprecation.target_album_id == self.target_album_id
        assert deprecation.status == self.status
        assert deprecation.done == self.done

    def test_equality(self):
        a = Deprecation(self.target_album_id, self.status, self.done)
        b = Deprecation(self.target_album_id, self.status, False)
        c = Deprecation(self.target_album_id, self.status, self.done)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
