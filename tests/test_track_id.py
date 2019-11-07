from yandex_music import TrackId


class TestTrackId:
    id = 74340
    album_id = 7025

    def test_expected_values(self, track_id, id):
        assert track_id.id == id
        assert track_id.album_id == self.album_id

    def test_de_json_required(self, client, id):
        json_dict = {'id': id}
        track_id = TrackId.de_json(json_dict, client)

        assert track_id.id == id

    def test_de_json_all(self, client, id):
        json_dict = {'id': id, 'album_id': self.album_id}
        track_id = TrackId.de_json(json_dict, client)

        assert track_id.id == id
        assert track_id.album_id == self.album_id

    def test_equality(self):
        a = TrackId(self.id, self.album_id)
        b = TrackId(10, self.album_id)
        c = TrackId(self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
