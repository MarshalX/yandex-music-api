from yandex_music import ArtistDonations


class TestArtistDonations:
    def test_expected_value(self, artist_donations, artist_donation_item):
        assert artist_donations.donations == [artist_donation_item]

    def test_de_json_none(self, client):
        assert ArtistDonations.de_json({}, client) is None

    def test_de_json_all(self, client, artist_donation_item):
        json_dict = {
            'donations': [artist_donation_item.to_dict()],
        }
        obj = ArtistDonations.de_json(json_dict, client)

        assert obj.donations == [artist_donation_item]

    def test_equality(self, artist_donation_item):
        a = ArtistDonations(donations=[artist_donation_item])
        b = ArtistDonations(donations=None)
        c = ArtistDonations(donations=[artist_donation_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
