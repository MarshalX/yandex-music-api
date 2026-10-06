from typing import Dict

from yandex_music import ArtistTrailerStatus, Client, JSONType


class TestArtistTrailerStatus:
    available = True

    def test_expected_value(self, artist_trailer_status: ArtistTrailerStatus) -> None:
        assert artist_trailer_status.available == self.available

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistTrailerStatus.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'available': self.available,
        }
        obj = ArtistTrailerStatus.de_json(json_dict, client)
        assert obj is not None

        assert obj.available == self.available

    def test_equality(self) -> None:
        a = ArtistTrailerStatus(available=True)
        b = ArtistTrailerStatus(available=False)
        c = ArtistTrailerStatus(available=True)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
