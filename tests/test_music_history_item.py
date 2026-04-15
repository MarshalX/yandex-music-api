from yandex_music import MusicHistoryItem


class TestMusicHistoryItem:
    type_track = 'track'
    type_album = 'album'

    def test_expected_value_track(self, music_history_item_track, music_history_item_data_track):
        assert music_history_item_track.type == self.type_track
        assert music_history_item_track.data == music_history_item_data_track

    def test_expected_value_album(self, music_history_item_album, music_history_item_data_context):
        assert music_history_item_album.type == self.type_album
        assert music_history_item_album.data == music_history_item_data_context

    def test_de_json_none(self, client):
        assert MusicHistoryItem.de_json({}, client) is None

    def test_de_json_track(self, client, music_history_item_id, track):
        json_dict = {
            'type': self.type_track,
            'data': {
                'itemId': music_history_item_id.to_dict(),
                'fullModel': track.to_dict(),
            },
        }
        obj = MusicHistoryItem.de_json(json_dict, client)
        assert obj.type == self.type_track
        assert obj.data.item_id == music_history_item_id
        assert obj.data.full_model == track

    def test_de_json_album(self, client, music_history_item_id, music_history_context_full_model_album):
        json_dict = {
            'type': self.type_album,
            'data': {
                'itemId': music_history_item_id.to_dict(),
                'fullModel': music_history_context_full_model_album.to_dict(),
            },
        }
        obj = MusicHistoryItem.de_json(json_dict, client)
        assert obj.type == self.type_album
        assert obj.data.item_id == music_history_item_id
        assert obj.data.full_model == music_history_context_full_model_album

    def test_de_list_none(self, client):
        assert MusicHistoryItem.de_list([], client) == []

    def test_equality(self, music_history_item_data_track):
        a = MusicHistoryItem(type=self.type_track, data=music_history_item_data_track)
        b = MusicHistoryItem(type=self.type_album, data=music_history_item_data_track)
        c = MusicHistoryItem(type=self.type_track, data=music_history_item_data_track)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
