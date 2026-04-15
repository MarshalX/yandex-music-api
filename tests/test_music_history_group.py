from yandex_music import MusicHistoryGroup


class TestMusicHistoryGroup:
    def test_expected_value(self, music_history_group, music_history_item_album, music_history_item_track):
        assert music_history_group.context == music_history_item_album
        assert music_history_group.tracks == [music_history_item_track]

    def test_de_json_none(self, client):
        assert MusicHistoryGroup.de_json({}, client) is None

    def test_de_json_all(self, client, music_history_item_album, music_history_item_track):
        json_dict = {
            'context': music_history_item_album.to_dict(),
            'tracks': [music_history_item_track.to_dict()],
        }
        obj = MusicHistoryGroup.de_json(json_dict, client)
        assert obj.context == music_history_item_album
        assert obj.tracks == [music_history_item_track]

    def test_de_list_none(self, client):
        assert MusicHistoryGroup.de_list([], client) == []

    def test_equality(self, music_history_item_album):
        a = MusicHistoryGroup(context=music_history_item_album)
        b = MusicHistoryGroup(context=None)
        c = MusicHistoryGroup(context=music_history_item_album)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
