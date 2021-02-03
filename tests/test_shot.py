from yandex_music import Shot


class TestShot:
    order = 0
    played = False
    shot_id = '1036797'
    status = 'ready'

    def test_expected_values(self, shot, shot_data):
        assert shot.order == self.order
        assert shot.played == self.played
        assert shot.shot_id == self.shot_id
        assert shot.status == self.status
        assert shot.shot_data == shot_data

    def test_de_json_none(self, client):
        assert Shot.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Shot.de_list({}, client) == []

    def test_de_json_required(self, client, shot_data):
        json_dict = {
            'order': self.order,
            'played': self.played,
            'shot_id': self.shot_id,
            'status': self.status,
            'shot_data': shot_data.to_dict(),
        }
        shot = Shot.de_json(json_dict, client)

        assert shot.order == self.order
        assert shot.played == self.played
        assert shot.shot_id == self.shot_id
        assert shot.status == self.status
        assert shot.shot_data == shot_data

    def test_de_json_all(self, client, shot_data):
        json_dict = {
            'order': self.order,
            'played': self.played,
            'shot_id': self.shot_id,
            'status': self.status,
            'shot_data': shot_data.to_dict(),
        }
        shot = Shot.de_json(json_dict, client)

        assert shot.order == self.order
        assert shot.played == self.played
        assert shot.shot_id == self.shot_id
        assert shot.status == self.status
        assert shot.shot_data == shot_data

    def test_equality(self, shot_data):
        a = Shot(self.order, self.played, shot_data, self.shot_id, self.status)
        b = Shot(self.order, True, shot_data, self.shot_id, self.status)
        c = Shot(self.order, self.played, shot_data, '10', self.status)
        d = Shot(self.order, self.played, shot_data, self.shot_id, self.status)

        assert a != b != c != d
        assert hash(a) != hash(b) != hash(c) != hash(d)
        assert a is not b is not c is not d

        assert a == d
        assert hash(a) == hash(d)
