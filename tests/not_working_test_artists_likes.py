import pytest

from yandex_music import ArtistsLikes


@pytest.fixture(scope='class')
def artists_likes(artist):
    return ArtistsLikes(TestArtistsLikes.id, artist, TestArtistsLikes.timestamp)


class TestArtistsLikes:
    timestamp = None

    def test_expected_values(self, artists_likes, id, artist):
        assert artists_likes.id == id
        assert artists_likes.artist == artist
        assert artists_likes.timestamp == self.timestamp

    def test_de_json_required(self, client):
        json_dict = {}
        artists_likes = ArtistsLikes.de_json(json_dict, client)

    def test_de_json_all(self, client, id, artist):
        json_dict = {'id': id, 'artist': artist, 'timestamp': self.timestamp}
        artists_likes = ArtistsLikes.de_json(json_dict, client)

        assert artists_likes.id == id
        assert artists_likes.artist == artist
        assert artists_likes.timestamp == self.timestamp

    def test_equality(self):
        pass
