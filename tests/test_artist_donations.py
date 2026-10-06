from typing import Dict

from yandex_music import ArtistDonationItem, ArtistDonations, Client, JSONType


class TestArtistDonations:
    def test_expected_value(self, artist_donations: ArtistDonations, artist_donation_item: ArtistDonationItem) -> None:
        assert artist_donations.donations == [artist_donation_item]

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistDonations.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist_donation_item: ArtistDonationItem) -> None:
        json_dict: Dict[str, JSONType] = {
            'donations': [artist_donation_item.to_dict()],
        }
        obj = ArtistDonations.de_json(json_dict, client)
        assert obj is not None

        assert obj.donations == [artist_donation_item]

    def test_equality(self, artist_donation_item: ArtistDonationItem) -> None:
        a = ArtistDonations(donations=[artist_donation_item])
        b = ArtistDonations(donations=None)
        c = ArtistDonations(donations=[artist_donation_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
