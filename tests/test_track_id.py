from yandex_music import TrackId


class TestTrackId:
    id = 74340
    track_id = 49947064
    album_id = 7025
    from_ = 'web-home_new-auto-playlist_of_the_day-playlist-main'

    def test_expected_values(self, track_id):
        assert track_id.id == self.id
        assert track_id.track_id == self.track_id
        assert track_id.album_id == self.album_id
        assert track_id.from_ == self.from_

    def test_de_json_none(self, client):
        assert TrackId.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert TrackId.de_list({}, client) == []

    def test_de_json_all(self, client):
        json_dict = {'id': self.id, 'track_id': self.track_id, 'album_id': self.album_id, 'from_': self.from_}
        track_id = TrackId.de_json(json_dict, client)

        assert track_id.id == self.id
        assert track_id.track_id == self.track_id
        assert track_id.album_id == self.album_id
        assert track_id.from_ == self.from_

    def test_equality(self):
        a = TrackId(self.id, self.album_id)
        b = TrackId(10, self.album_id)
        c = TrackId(self.id, self.album_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
