from yandex_music import CombinedSessionItem


class TestCombinedSessionItem:
    type = 'CLIP'

    def test_expected_values(self, combined_session_item, clip):
        assert combined_session_item.type == self.type
        assert combined_session_item.data == clip

    def test_de_json_none(self, client):
        assert CombinedSessionItem.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert CombinedSessionItem.de_list([], client) == []

    def test_de_json_clip(self, client, clip):
        json_dict = {'type': self.type, 'data': clip.to_dict()}
        combined_session_item = CombinedSessionItem.de_json(json_dict, client)

        assert combined_session_item.type == self.type
        assert combined_session_item.data == clip

    def test_de_json_track(self, client, track):
        json_dict = {'type': 'TRACK', 'data': track.to_dict()}
        combined_session_item = CombinedSessionItem.de_json(json_dict, client)

        assert combined_session_item.type == 'TRACK'
        assert combined_session_item.data == track

    def test_de_json_unknown_type(self, client, clip):
        json_dict = {'type': 'UNKNOWN', 'data': clip.to_dict()}
        combined_session_item = CombinedSessionItem.de_json(json_dict, client)

        assert combined_session_item.type == 'UNKNOWN'
        assert combined_session_item.data is None

    def test_equality(self, clip, track):
        a = CombinedSessionItem(self.type, clip)
        b = CombinedSessionItem('TRACK', track)
        c = CombinedSessionItem(self.type, clip)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
