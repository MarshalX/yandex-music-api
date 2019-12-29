from yandex_music import PlaylistId


class TestPlaylistId:
    uid = 460142547
    kind = 5332052

    def test_expected_values(self, playlist_id):
        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_de_json_none(self, client):
        assert PlaylistId.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert PlaylistId.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'uid': self.uid, 'kind': self.kind}
        playlist_id = PlaylistId.de_json(json_dict, client)

        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_de_json_all(self, client):
        json_dict = {'uid': self.uid, 'kind': self.kind}
        playlist_id = PlaylistId.de_json(json_dict, client)

        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_equality(self):
        a = PlaylistId(self.uid, self.kind)
        b = PlaylistId(self.uid, 10)
        c = PlaylistId(10, self.kind)
        d = PlaylistId(self.uid, self.kind)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
