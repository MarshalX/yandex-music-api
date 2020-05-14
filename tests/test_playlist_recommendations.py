import pytest

from yandex_music import PlaylistRecommendations


@pytest.fixture(scope='class')
def playlist_recommendations(track):
    return PlaylistRecommendations([track], TestPlaylistRecommendations.batch_id)


class TestPlaylistRecommendations:
    batch_id = '1588835234913188-6341822935848536902'

    def test_expected_values(self, playlist_recommendations, track):
        assert playlist_recommendations.batch_id == self.batch_id
        assert playlist_recommendations.tracks == [track]

    def test_de_json_none(self, client):
        assert PlaylistRecommendations.de_json({}, client) is None

    def test_de_json_required(self, client, track):
        json_dict = {'tracks': [track.to_dict()]}
        playlist_recommendations = PlaylistRecommendations.de_json(json_dict, client)

        assert playlist_recommendations.tracks == [track]

    def test_de_json_all(self, client, track):
        json_dict = {'batch_id': self.batch_id, 'tracks': [track.to_dict()]}
        playlist_recommendations = PlaylistRecommendations.de_json(json_dict, client)

        assert playlist_recommendations.batch_id == self.batch_id
        assert playlist_recommendations.tracks == [track]

    def test_equality(self, track):
        a = PlaylistRecommendations([track])
        b = PlaylistRecommendations([])
        c = PlaylistRecommendations([track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
