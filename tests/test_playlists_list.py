from yandex_music import PlaylistsList


class TestPlaylistsList:
    def test_expected_value(self, playlists_list, playlist):
        assert playlists_list.playlists == [playlist]

    def test_de_json_none(self, client):
        assert PlaylistsList.de_json({}, client) is None

    def test_de_json_all(self, client, playlist):
        json_dict = {
            'playlists': [playlist.to_dict()],
        }
        playlists_list = PlaylistsList.de_json(json_dict, client)

        assert playlists_list.playlists == [playlist]

    def test_equality(self, playlist):
        a = PlaylistsList(playlists=[playlist])
        b = PlaylistsList(playlists=None)
        c = PlaylistsList(playlists=[playlist])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
