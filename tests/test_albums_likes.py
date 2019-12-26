import pytest

from yandex_music import AlbumsLikes


@pytest.fixture(scope='class')
def albums_likes(album):
    return AlbumsLikes(TestAlbumsLikes.timestamp, TestAlbumsLikes.id, album)


class TestAlbumsLikes:
    id = 5246018
    timestamp = '2019-09-03T19:59:56+00:00'

    def test_expected_values(self, albums_likes, album):
        assert albums_likes.timestamp == self.timestamp
        assert albums_likes.id == self.id
        assert albums_likes.album == album

    def test_de_json_required(self, client):
        json_dict = {'timestamp': self.timestamp}
        albums_likes = AlbumsLikes.de_json(json_dict, client)

        assert albums_likes.timestamp == self.timestamp

    def test_de_json_all(self, client, album):
        json_dict = {'timestamp': self.timestamp, 'id_': self.id, 'album': album.to_dict()}
        albums_likes = AlbumsLikes.de_json(json_dict, client)

        assert albums_likes.timestamp == self.timestamp
        assert albums_likes.id == self.id
        assert albums_likes.album == album

    def test_equality(self, album):
        a = AlbumsLikes(self.timestamp, self.id, album)
        b = AlbumsLikes(self.timestamp, self.id, None)
        c = AlbumsLikes(self.timestamp, self.id, album)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
