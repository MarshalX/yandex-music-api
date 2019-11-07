import pytest

from yandex_music import PlayContextsData


@pytest.fixture(scope='class')
def play_contexts_data(other_tracks):
    return PlayContextsData(other_tracks)


class TestPlayContextsData:

    def test_expected_values(self, play_contexts_data, other_tracks):
        assert play_contexts_data.other_tracks == other_tracks

    def test_de_json_required(self, client, other_tracks):
        json_dict = {'other_tracks': other_tracks}
        play_contexts_data = PlayContextsData.de_json(json_dict, client)

        assert play_contexts_data.other_tracks == other_tracks

    def test_de_json_all(self, client, other_tracks):
        json_dict = {'other_tracks': other_tracks}
        play_contexts_data = PlayContextsData.de_json(json_dict, client)

        assert play_contexts_data.other_tracks == other_tracks

    def test_equality(self):
        pass
