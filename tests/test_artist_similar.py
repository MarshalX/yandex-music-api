from yandex_music import ArtistSimilar


class TestArtistSimilar:
    def test_expected_value(self, artist_similar, artist):
        assert artist_similar.artist == artist
        assert artist_similar.similar_artists == [artist]

    def test_de_json_none(self, client):
        assert ArtistSimilar.de_json({}, client) is None

    def test_de_json_all(self, client, artist):
        json_dict = {
            'artist': artist.to_dict(),
            'similarArtists': [artist.to_dict()],
        }
        artist_similar = ArtistSimilar.de_json(json_dict, client)

        assert artist_similar.artist == artist
        assert artist_similar.similar_artists == [artist]

    def test_equality(self, artist):
        a = ArtistSimilar(artist=artist)
        b = ArtistSimilar(artist=None)
        c = ArtistSimilar(artist=artist)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
