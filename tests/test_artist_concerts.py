from typing import Dict

from yandex_music import ArtistConcerts, Client, Concert, JSONType


class TestArtistConcerts:
    artist_title = 'Кино'

    def test_expected_value(self, artist_concerts: ArtistConcerts, concert: Concert) -> None:
        assert artist_concerts.artist_title == self.artist_title
        assert artist_concerts.concerts == [concert]

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistConcerts.de_json({}, client) is None

    def test_de_json_all(self, client: Client, concert: Concert) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist_title': self.artist_title,
            'concerts': [concert.to_dict()],
        }
        artist_concerts = ArtistConcerts.de_json(json_dict, client)
        assert artist_concerts is not None

        assert artist_concerts.artist_title == self.artist_title
        assert artist_concerts.concerts == [concert]

    def test_equality(self, concert: Concert) -> None:
        a = ArtistConcerts(artist_title=self.artist_title, concerts=[concert])
        b = ArtistConcerts(artist_title='Другой артист', concerts=[])
        c = ArtistConcerts(artist_title=self.artist_title, concerts=[concert])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
