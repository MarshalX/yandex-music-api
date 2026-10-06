from typing import Dict

from yandex_music import Artist, ArtistTrailer, Client, JSONType, TrailerInfo


class TestArtistTrailer:
    def test_expected_value(self, artist_trailer: ArtistTrailer, artist: Artist, trailer_info: TrailerInfo) -> None:
        assert artist_trailer.artist == artist
        assert artist_trailer.trailer == trailer_info

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistTrailer.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist: Artist, trailer_info: TrailerInfo) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'trailer': trailer_info.to_dict(),
        }
        obj = ArtistTrailer.de_json(json_dict, client)
        assert obj is not None

        assert obj.artist == artist
        assert obj.trailer == trailer_info

    def test_equality(self, artist: Artist, trailer_info: TrailerInfo) -> None:
        a = ArtistTrailer(artist=artist, trailer=trailer_info)
        b = ArtistTrailer(artist=None, trailer=None)
        c = ArtistTrailer(artist=artist, trailer=trailer_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
