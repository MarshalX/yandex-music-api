from yandex_music import ArtistTrailer


class TestArtistTrailer:
    def test_expected_value(self, artist_trailer, artist, trailer_info):
        assert artist_trailer.artist == artist
        assert artist_trailer.trailer == trailer_info

    def test_de_json_none(self, client):
        assert ArtistTrailer.de_json({}, client) is None

    def test_de_json_all(self, client, artist, trailer_info):
        json_dict = {
            'artist': artist.to_dict(),
            'trailer': trailer_info.to_dict(),
        }
        obj = ArtistTrailer.de_json(json_dict, client)

        assert obj.artist == artist
        assert obj.trailer == trailer_info

    def test_equality(self, artist, trailer_info):
        a = ArtistTrailer(artist=artist, trailer=trailer_info)
        b = ArtistTrailer(artist=None, trailer=None)
        c = ArtistTrailer(artist=artist, trailer=trailer_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
