from typing import Dict

from yandex_music import ArtistDonationData, ArtistDonationItem, Client, JSONType


class TestArtistDonationItem:
    type = 'donation_item'

    def test_expected_value(
        self, artist_donation_item: ArtistDonationItem, artist_donation_data: ArtistDonationData
    ) -> None:
        assert artist_donation_item.type == self.type
        assert artist_donation_item.data == artist_donation_data

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistDonationItem.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist_donation_data: ArtistDonationData) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'data': artist_donation_data.to_dict(),
        }
        obj = ArtistDonationItem.de_json(json_dict, client)
        assert obj is not None

        assert obj.type == self.type
        assert obj.data == artist_donation_data

    def test_equality(self, artist_donation_data: ArtistDonationData) -> None:
        a = ArtistDonationItem(type='donation_item', data=artist_donation_data)
        b = ArtistDonationItem(type='donation_item', data=None)
        c = ArtistDonationItem(type='donation_item', data=artist_donation_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
