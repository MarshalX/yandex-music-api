import pytest

from yandex_music import ArtistsLikes


@pytest.fixture(scope='class')
def artists_likes(artist):
    return ArtistsLikes(TestArtistsLikes.id, artist, TestArtistsLikes.timestamp)


class TestArtistsLikes:
    id = None
    timestamp = '2019-11-09T10:28:39+00:00'

    def test_expected_values(self, artists_likes, artist):
        assert artists_likes.id == self.id
        assert artists_likes.artist == artist
        assert artists_likes.timestamp == self.timestamp

    def test_de_json_none(self, client):
        assert ArtistsLikes.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert ArtistsLikes.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {}
        artists_likes = ArtistsLikes.de_json(json_dict, client)

    def test_de_json_all(self, client, artist):
        json_dict = {'id_': self.id, 'artist': artist.to_dict(), 'timestamp': self.timestamp}
        artists_likes = ArtistsLikes.de_json(json_dict, client)

        assert artists_likes.id == self.id
        assert artists_likes.artist == artist
        assert artists_likes.timestamp == self.timestamp

    def test_equality(self, artist):
        a = ArtistsLikes(self.id, artist, self.timestamp)
        b = ArtistsLikes(self.id, None, self.timestamp)
        c = ArtistsLikes(self.id, artist, self.timestamp)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
