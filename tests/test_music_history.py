from yandex_music import MusicHistory


class TestMusicHistory:
    def test_expected_value(self, music_history, music_history_tab):
        assert music_history.history_tabs == [music_history_tab]

    def test_de_json_none(self, client):
        assert MusicHistory.de_json({}, client) is None

    def test_de_json_all(self, client, music_history_tab):
        json_dict = {
            'historyTabs': [music_history_tab.to_dict()],
        }
        obj = MusicHistory.de_json(json_dict, client)
        assert obj.history_tabs == [music_history_tab]

    def test_equality(self, music_history_tab):
        a = MusicHistory(history_tabs=[music_history_tab])
        b = MusicHistory(history_tabs=None)
        c = MusicHistory(history_tabs=[music_history_tab])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
