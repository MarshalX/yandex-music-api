from yandex_music import ArtistConcerts


class TestArtistConcerts:
    artist_title = 'Кино'

    def test_expected_value(self, artist_concerts, concert):
        assert artist_concerts.artist_title == self.artist_title
        assert artist_concerts.concerts == [concert]

    def test_de_json_none(self, client):
        assert ArtistConcerts.de_json({}, client) is None

    def test_de_json_all(self, client, concert):
        json_dict = {
            'artist_title': self.artist_title,
            'concerts': [concert.to_dict()],
        }
        artist_concerts = ArtistConcerts.de_json(json_dict, client)

        assert artist_concerts.artist_title == self.artist_title
        assert artist_concerts.concerts == [concert]

    def test_equality(self, concert):
        a = ArtistConcerts(artist_title=self.artist_title, concerts=[concert])
        b = ArtistConcerts(artist_title='Другой артист', concerts=[])
        c = ArtistConcerts(artist_title=self.artist_title, concerts=[concert])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
