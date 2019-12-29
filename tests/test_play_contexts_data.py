from yandex_music import PlayContextsData


class TestPlayContextsData:
    def test_expected_values(self, play_contexts_data, track_short_old):
        assert play_contexts_data.other_tracks == [track_short_old]

    def test_de_json_none(self, client):
        assert PlayContextsData.de_json({}, client) is None

    def test_de_json_required(self, client, track_short_old):
        json_dict = {'other_tracks': [track_short_old.to_dict()]}
        play_contexts_data = PlayContextsData.de_json(json_dict, client)

        assert play_contexts_data.other_tracks == [track_short_old]

    def test_de_json_all(self, client, track_short_old):
        json_dict = {'other_tracks': [track_short_old.to_dict()]}
        play_contexts_data = PlayContextsData.de_json(json_dict, client)

        assert play_contexts_data.other_tracks == [track_short_old]

    def test_equality(self, track_short_old):
        a = PlayContextsData([track_short_old])
        b = PlayContextsData([])

        assert a != b != track_short_old
        assert hash(a) != hash(b) != hash(track_short_old)
        assert a is not track_short_old
