import pytest

from yandex_music import PlaylistsLikes


@pytest.fixture(scope='class')
def playlists_likes(playlist):
    return PlaylistsLikes(TestPlaylistsLikes.timestamp, TestPlaylistsLikes.id, playlist)


class TestPlaylistsLikes:
    timestamp = None

    def test_expected_values(self, playlists_likes, id, playlist):
        assert playlists_likes.timestamp == self.timestamp
        assert playlists_likes.id == id
        assert playlists_likes.playlist == playlist

    def test_de_json_required(self, client):
        json_dict = {'timestamp': self.timestamp}
        playlists_likes = PlaylistsLikes.de_json(json_dict, client)

        assert playlists_likes.timestamp == self.timestamp

    def test_de_json_all(self, client, id, playlist):
        json_dict = {'timestamp': self.timestamp, 'id': id, 'playlist': playlist}
        playlists_likes = PlaylistsLikes.de_json(json_dict, client)

        assert playlists_likes.timestamp == self.timestamp
        assert playlists_likes.id == id
        assert playlists_likes.playlist == playlist

    def test_equality(self):
        pass
