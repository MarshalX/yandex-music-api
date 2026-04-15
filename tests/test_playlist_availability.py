from yandex_music import PlaylistAvailability


class TestPlaylistAvailability:
    available = False

    def test_expected_values(self, playlist_availability):
        assert playlist_availability.available == self.available

    def test_de_json_none(self, client):
        assert PlaylistAvailability.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'available': self.available,
        }
        playlist_availability = PlaylistAvailability.de_json(json_dict, client)

        assert playlist_availability.available == self.available

    def test_equality(self):
        a = PlaylistAvailability(available=False)
        b = PlaylistAvailability(available=True)
        c = PlaylistAvailability(available=False)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
