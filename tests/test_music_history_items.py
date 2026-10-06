from typing import Dict

from yandex_music import Client, JSONType, MusicHistoryItem, MusicHistoryItems


class TestMusicHistoryItems:
    def test_expected_value(
        self, music_history_items: MusicHistoryItems, music_history_item_track: MusicHistoryItem
    ) -> None:
        assert music_history_items.items == [music_history_item_track]

    def test_de_json_none(self, client: Client) -> None:
        assert MusicHistoryItems.de_json({}, client) is None

    def test_de_json_all(self, client: Client, music_history_item_track: MusicHistoryItem) -> None:
        json_dict: Dict[str, JSONType] = {
            'items': [music_history_item_track.to_dict()],
        }
        obj = MusicHistoryItems.de_json(json_dict, client)
        assert obj is not None
        assert obj.items == [music_history_item_track]

    def test_equality(self, music_history_item_track: MusicHistoryItem) -> None:
        a = MusicHistoryItems(items=[music_history_item_track])
        b = MusicHistoryItems(items=None)
        c = MusicHistoryItems(items=[music_history_item_track])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
