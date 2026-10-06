from typing import Dict

from yandex_music import Album, AlbumTrailer, Artist, Client, JSONType, TrailerInfo


class TestAlbumTrailer:
    def test_expected_values(
        self, album_trailer: AlbumTrailer, album: Album, artist: Artist, trailer_info: TrailerInfo
    ) -> None:
        assert album_trailer.album == album
        assert album_trailer.artists == [artist]
        assert album_trailer.trailer == trailer_info

    def test_de_json_none(self, client: Client) -> None:
        assert AlbumTrailer.de_json({}, client) is None

    def test_de_json_all(self, client: Client, album: Album, artist: Artist, trailer_info: TrailerInfo) -> None:
        json_dict: Dict[str, JSONType] = {
            'album': album.to_dict(),
            'artists': [artist.to_dict()],
            'trailer': trailer_info.to_dict(),
        }
        trailer = AlbumTrailer.de_json(json_dict, client)
        assert trailer is not None

        assert trailer.album == album
        assert trailer.artists == [artist]
        assert trailer.trailer == trailer_info

    def test_equality(self, album: Album, trailer_info: TrailerInfo) -> None:
        a = AlbumTrailer(album=album, trailer=trailer_info)
        b = AlbumTrailer(album=None, trailer=trailer_info)
        c = AlbumTrailer(album=album, trailer=trailer_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
