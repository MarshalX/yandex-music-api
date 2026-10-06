from typing import Dict

from yandex_music import Artist, ArtistSimilar, Client, JSONType


class TestArtistSimilar:
    def test_expected_value(self, artist_similar: ArtistSimilar, artist: Artist) -> None:
        assert artist_similar.artist == artist
        assert artist_similar.similar_artists == [artist]

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistSimilar.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist: Artist) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'similarArtists': [artist.to_dict()],
        }
        artist_similar = ArtistSimilar.de_json(json_dict, client)
        assert artist_similar is not None

        assert artist_similar.artist == artist
        assert artist_similar.similar_artists == [artist]

    def test_equality(self, artist: Artist) -> None:
        a = ArtistSimilar(artist=artist)
        b = ArtistSimilar(artist=None)
        c = ArtistSimilar(artist=artist)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
