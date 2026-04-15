from yandex_music import AlbumTrailer


class TestAlbumTrailer:
    def test_expected_values(self, album_trailer, album, artist, trailer_info):
        assert album_trailer.album == album
        assert album_trailer.artists == [artist]
        assert album_trailer.trailer == trailer_info

    def test_de_json_none(self, client):
        assert AlbumTrailer.de_json({}, client) is None

    def test_de_json_all(self, client, album, artist, trailer_info):
        json_dict = {
            'album': album.to_dict(),
            'artists': [artist.to_dict()],
            'trailer': trailer_info.to_dict(),
        }
        trailer = AlbumTrailer.de_json(json_dict, client)

        assert trailer.album == album
        assert trailer.artists == [artist]
        assert trailer.trailer == trailer_info

    def test_equality(self, album, trailer_info):
        a = AlbumTrailer(album=album, trailer=trailer_info)
        b = AlbumTrailer(album=None, trailer=trailer_info)
        c = AlbumTrailer(album=album, trailer=trailer_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
