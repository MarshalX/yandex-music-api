from typing import Dict

from yandex_music import Client, JSONType, MusicHistoryContextFullModel, MusicHistoryItemData, MusicHistoryItemId, Track


class TestMusicHistoryItemData:
    def test_expected_value_track(
        self,
        music_history_item_data_track: MusicHistoryItemData,
        music_history_item_id: MusicHistoryItemId,
        track: Track,
    ) -> None:
        assert music_history_item_data_track.item_id == music_history_item_id
        assert music_history_item_data_track.full_model == track

    def test_expected_value_context(
        self,
        music_history_item_data_context: MusicHistoryItemData,
        music_history_item_id: MusicHistoryItemId,
        music_history_context_full_model_album: MusicHistoryContextFullModel,
    ) -> None:
        assert music_history_item_data_context.item_id == music_history_item_id
        assert music_history_item_data_context.full_model == music_history_context_full_model_album

    def test_de_json_none(self, client: Client) -> None:
        assert MusicHistoryItemData.de_json({}, client) is None

    def test_de_json_track(self, client: Client, music_history_item_id: MusicHistoryItemId, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'itemId': music_history_item_id.to_dict(),
            'fullModel': track.to_dict(),
        }
        obj = MusicHistoryItemData.de_json(json_dict, client, item_type='track')
        assert obj is not None
        assert obj.item_id == music_history_item_id
        assert obj.full_model == track

    def test_de_json_album(
        self,
        client: Client,
        music_history_item_id: MusicHistoryItemId,
        music_history_context_full_model_album: MusicHistoryContextFullModel,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'itemId': music_history_item_id.to_dict(),
            'fullModel': music_history_context_full_model_album.to_dict(),
        }
        obj = MusicHistoryItemData.de_json(json_dict, client, item_type='album')
        assert obj is not None
        assert obj.item_id == music_history_item_id
        assert obj.full_model == music_history_context_full_model_album

    def test_equality(self, music_history_item_id: MusicHistoryItemId) -> None:
        a = MusicHistoryItemData(item_id=music_history_item_id)
        b = MusicHistoryItemData(item_id=None)
        c = MusicHistoryItemData(item_id=music_history_item_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
