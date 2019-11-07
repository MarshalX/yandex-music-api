from yandex_music import TrackId


class TestTrackId:
    album_id = None

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
        pass
