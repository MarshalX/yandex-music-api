from typing import Dict

from yandex_music import Artist, ArtistDonationData, ArtistDonationGoal, Client, JSONType


class TestArtistDonationData:
    tip_url = 'https://tips.yandex.ru/guest/payment/12345'

    def test_expected_value(
        self, artist_donation_data: ArtistDonationData, artist: Artist, artist_donation_goal: ArtistDonationGoal
    ) -> None:
        assert artist_donation_data.tip_url == self.tip_url
        assert artist_donation_data.artist == artist
        assert artist_donation_data.goal == artist_donation_goal

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistDonationData.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist: Artist, artist_donation_goal: ArtistDonationGoal) -> None:
        json_dict: Dict[str, JSONType] = {
            'tipUrl': self.tip_url,
            'artist': artist.to_dict(),
            'goal': artist_donation_goal.to_dict(),
        }
        obj = ArtistDonationData.de_json(json_dict, client)
        assert obj is not None

        assert obj.tip_url == self.tip_url
        assert obj.artist == artist
        assert obj.goal == artist_donation_goal

    def test_equality(self) -> None:
        a = ArtistDonationData(tip_url='https://example.com/1')
        b = ArtistDonationData(tip_url='https://example.com/2')
        c = ArtistDonationData(tip_url='https://example.com/1')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
