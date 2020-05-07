import pytest

from yandex_music import PlaylistsRecommendations


@pytest.fixture(scope='class')
def playlists_recommendations(track):
    return PlaylistsRecommendations([track], TestPlaylistsRecommendations.batch_id)


class TestPlaylistsRecommendations:
    batch_id = '1588835234913188-6341822935848536902'

    def test_expected_values(self, playlists_recommendations, track):
        assert playlists_recommendations.batch_id == self.batch_id
        assert playlists_recommendations.tracks == [track]

    def test_de_json_none(self, client):
        assert PlaylistsRecommendations.de_json({}, client) is None

    def test_de_json_required(self, client, track):
        json_dict = {'tracks': [track.to_dict()]}
        playlists_recommendations = PlaylistsRecommendations.de_json(json_dict, client)

        assert playlists_recommendations.tracks == [track]

    def test_de_json_all(self, client, track):
        json_dict = {'batch_id': self.batch_id, 'tracks': [track.to_dict()]}
        playlists_recommendations = PlaylistsRecommendations.de_json(json_dict, client)

        assert playlists_recommendations.batch_id == self.batch_id
        assert playlists_recommendations.tracks == [track]

    def test_equality(self, track):
        a = PlaylistsRecommendations([track])
        b = PlaylistsRecommendations([])
        c = PlaylistsRecommendations([track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
