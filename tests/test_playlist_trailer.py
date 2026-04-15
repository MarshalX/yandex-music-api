from yandex_music import PlaylistTrailer


class TestPlaylistTrailer:
    shareable = False

    def test_expected_values(self, playlist_trailer, playlist, trailer_info):
        assert playlist_trailer.playlist == playlist
        assert playlist_trailer.trailer == trailer_info
        assert playlist_trailer.shareable == self.shareable

    def test_de_json_none(self, client):
        assert PlaylistTrailer.de_json({}, client) is None

    def test_de_json_all(self, client, playlist, trailer_info):
        json_dict = {
            'playlist': playlist.to_dict(),
            'trailer': trailer_info.to_dict(),
            'shareable': self.shareable,
        }
        playlist_trailer = PlaylistTrailer.de_json(json_dict, client)

        assert playlist_trailer.playlist == playlist
        assert playlist_trailer.trailer == trailer_info
        assert playlist_trailer.shareable == self.shareable

    def test_equality(self, playlist, trailer_info):
        a = PlaylistTrailer(playlist=playlist, trailer=trailer_info)
        b = PlaylistTrailer(playlist=None, trailer=trailer_info)
        c = PlaylistTrailer(playlist=playlist, trailer=trailer_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
