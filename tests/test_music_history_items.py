from yandex_music import MusicHistoryItems


class TestMusicHistoryItems:
    def test_expected_value(self, music_history_items, music_history_item_track):
        assert music_history_items.items == [music_history_item_track]

    def test_de_json_none(self, client):
        assert MusicHistoryItems.de_json({}, client) is None

    def test_de_json_all(self, client, music_history_item_track):
        json_dict = {
            'items': [music_history_item_track.to_dict()],
        }
        obj = MusicHistoryItems.de_json(json_dict, client)
        assert obj.items == [music_history_item_track]

    def test_equality(self, music_history_item_track):
        a = MusicHistoryItems(items=[music_history_item_track])
        b = MusicHistoryItems(items=None)
        c = MusicHistoryItems(items=[music_history_item_track])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
