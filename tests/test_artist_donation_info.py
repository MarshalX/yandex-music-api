from typing import Dict

from yandex_music import ArtistDonationInfo, Client, JSONType


class TestArtistDonationInfo:
    title = 'Поддержать артиста'
    url = 'https://example.com/donate/100500'

    def test_expected_values(self, artist_donation_info: ArtistDonationInfo) -> None:
        assert artist_donation_info.title == self.title
        assert artist_donation_info.url == self.url

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistDonationInfo.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'title': self.title, 'url': self.url}
        obj = ArtistDonationInfo.de_json(json_dict, client)
        assert obj is not None

        assert obj.title == self.title
        assert obj.url == self.url

    def test_equality(self) -> None:
        a = ArtistDonationInfo(title=self.title, url=self.url)
        b = ArtistDonationInfo(title=self.title, url='https://example.com/other')
        c = ArtistDonationInfo(title=self.title, url=self.url)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
