from typing import Dict

from yandex_music import Client, JSONType, MusicHistory, MusicHistoryTab


class TestMusicHistory:
    def test_expected_value(self, music_history: MusicHistory, music_history_tab: MusicHistoryTab) -> None:
        assert music_history.history_tabs == [music_history_tab]

    def test_de_json_none(self, client: Client) -> None:
        assert MusicHistory.de_json({}, client) is None

    def test_de_json_all(self, client: Client, music_history_tab: MusicHistoryTab) -> None:
        json_dict: Dict[str, JSONType] = {
            'historyTabs': [music_history_tab.to_dict()],
        }
        obj = MusicHistory.de_json(json_dict, client)
        assert obj is not None
        assert obj.history_tabs == [music_history_tab]

    def test_equality(self, music_history_tab: MusicHistoryTab) -> None:
        a = MusicHistory(history_tabs=[music_history_tab])
        b = MusicHistory(history_tabs=None)
        c = MusicHistory(history_tabs=[music_history_tab])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
