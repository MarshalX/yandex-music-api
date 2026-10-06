from typing import Dict

from yandex_music import Client, JSONType, PlaylistAvailability


class TestPlaylistAvailability:
    available = False

    def test_expected_values(self, playlist_availability: PlaylistAvailability) -> None:
        assert playlist_availability.available == self.available

    def test_de_json_none(self, client: Client) -> None:
        assert PlaylistAvailability.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'available': self.available,
        }
        playlist_availability = PlaylistAvailability.de_json(json_dict, client)
        assert playlist_availability is not None

        assert playlist_availability.available == self.available

    def test_equality(self) -> None:
        a = PlaylistAvailability(available=False)
        b = PlaylistAvailability(available=True)
        c = PlaylistAvailability(available=False)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
