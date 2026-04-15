from yandex_music import ArtistTrailerStatus


class TestArtistTrailerStatus:
    available = True

    def test_expected_value(self, artist_trailer_status):
        assert artist_trailer_status.available == self.available

    def test_de_json_none(self, client):
        assert ArtistTrailerStatus.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'available': self.available,
        }
        obj = ArtistTrailerStatus.de_json(json_dict, client)

        assert obj.available == self.available

    def test_equality(self):
        a = ArtistTrailerStatus(available=True)
        b = ArtistTrailerStatus(available=False)
        c = ArtistTrailerStatus(available=True)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
