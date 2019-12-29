import pytest

from yandex_music import PlaylistsLikes


@pytest.fixture(scope='class')
def playlists_likes(playlist):
    return PlaylistsLikes(TestPlaylistsLikes.timestamp, TestPlaylistsLikes.id, playlist)


class TestPlaylistsLikes:
    id = None
    timestamp = '2019-06-21T05:41:46+00:00'

    def test_expected_values(self, playlists_likes, playlist):
        assert playlists_likes.timestamp == self.timestamp
        assert playlists_likes.id == self.id
        assert playlists_likes.playlist == playlist

    def test_de_json_none(self, client):
        assert PlaylistsLikes.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'timestamp': self.timestamp}
        playlists_likes = PlaylistsLikes.de_json(json_dict, client)

        assert playlists_likes.timestamp == self.timestamp

    def test_de_json_all(self, client, playlist):
        json_dict = {'timestamp': self.timestamp, 'id_': self.id, 'playlist': playlist.to_dict()}
        playlists_likes = PlaylistsLikes.de_json(json_dict, client)

        assert playlists_likes.timestamp == self.timestamp
        assert playlists_likes.id == self.id
        assert playlists_likes.playlist == playlist

    def test_equality(self, playlist):
        a = PlaylistsLikes(self.timestamp, self.id, playlist)
        b = PlaylistsLikes(self.timestamp, self.id, None)
        c = PlaylistsLikes(self.timestamp, self.id, playlist)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
