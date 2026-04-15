from yandex_music import ArtistDonationItem


class TestArtistDonationItem:
    type = 'donation_item'

    def test_expected_value(self, artist_donation_item, artist_donation_data):
        assert artist_donation_item.type == self.type
        assert artist_donation_item.data == artist_donation_data

    def test_de_json_none(self, client):
        assert ArtistDonationItem.de_json({}, client) is None

    def test_de_json_all(self, client, artist_donation_data):
        json_dict = {
            'type': self.type,
            'data': artist_donation_data.to_dict(),
        }
        obj = ArtistDonationItem.de_json(json_dict, client)

        assert obj.type == self.type
        assert obj.data == artist_donation_data

    def test_equality(self, artist_donation_data):
        a = ArtistDonationItem(type='donation_item', data=artist_donation_data)
        b = ArtistDonationItem(type='donation_item', data=None)
        c = ArtistDonationItem(type='donation_item', data=artist_donation_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
