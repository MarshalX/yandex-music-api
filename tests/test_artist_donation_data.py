from yandex_music import ArtistDonationData


class TestArtistDonationData:
    tip_url = 'https://tips.yandex.ru/guest/payment/12345'

    def test_expected_value(self, artist_donation_data, artist, artist_donation_goal):
        assert artist_donation_data.tip_url == self.tip_url
        assert artist_donation_data.artist == artist
        assert artist_donation_data.goal == artist_donation_goal

    def test_de_json_none(self, client):
        assert ArtistDonationData.de_json({}, client) is None

    def test_de_json_all(self, client, artist, artist_donation_goal):
        json_dict = {
            'tipUrl': self.tip_url,
            'artist': artist.to_dict(),
            'goal': artist_donation_goal.to_dict(),
        }
        obj = ArtistDonationData.de_json(json_dict, client)

        assert obj.tip_url == self.tip_url
        assert obj.artist == artist
        assert obj.goal == artist_donation_goal

    def test_equality(self):
        a = ArtistDonationData(tip_url='https://example.com/1')
        b = ArtistDonationData(tip_url='https://example.com/2')
        c = ArtistDonationData(tip_url='https://example.com/1')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
