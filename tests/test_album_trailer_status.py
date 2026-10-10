from typing import Dict

from yandex_music import AlbumTrailerStatus, Client, JSONType


class TestAlbumTrailerStatus:
    available = True

    def test_expected_value(self, album_trailer_status: AlbumTrailerStatus) -> None:
        assert album_trailer_status.available == self.available

    def test_de_json_none(self, client: Client) -> None:
        assert AlbumTrailerStatus.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'available': self.available,
        }
        obj = AlbumTrailerStatus.de_json(json_dict, client)
        assert obj is not None

        assert obj.available == self.available

    def test_equality(self) -> None:
        a = AlbumTrailerStatus(available=True)
        b = AlbumTrailerStatus(available=False)
        c = AlbumTrailerStatus(available=True)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
