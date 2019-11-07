import pytest

from yandex_music import AlbumsLikes


@pytest.fixture(scope='class')
def albums_likes(album):
    return AlbumsLikes(TestAlbumsLikes.timestamp, TestAlbumsLikes.id, album)


class TestAlbumsLikes:
    timestamp = None

    def test_expected_values(self, albums_likes, id, album):
        assert albums_likes.timestamp == self.timestamp
        assert albums_likes.id == id
        assert albums_likes.album == album

    def test_de_json_required(self, client):
        json_dict = {'timestamp': self.timestamp}
        albums_likes = AlbumsLikes.de_json(json_dict, client)

        assert albums_likes.timestamp == self.timestamp

    def test_de_json_all(self, client, id, album):
        json_dict = {'timestamp': self.timestamp, 'id': id, 'album': album}
        albums_likes = AlbumsLikes.de_json(json_dict, client)

        assert albums_likes.timestamp == self.timestamp
        assert albums_likes.id == id
        assert albums_likes.album == album

    def test_equality(self):
        pass
