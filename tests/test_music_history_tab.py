from yandex_music import MusicHistoryTab


class TestMusicHistoryTab:
    date = '2025-01-15'

    def test_expected_value(self, music_history_tab, music_history_group):
        assert music_history_tab.date == self.date
        assert music_history_tab.items == [music_history_group]

    def test_de_json_none(self, client):
        assert MusicHistoryTab.de_json({}, client) is None

    def test_de_json_all(self, client, music_history_group):
        json_dict = {
            'date': self.date,
            'items': [music_history_group.to_dict()],
        }
        obj = MusicHistoryTab.de_json(json_dict, client)
        assert obj.date == self.date
        assert obj.items == [music_history_group]

    def test_de_list_none(self, client):
        assert MusicHistoryTab.de_list([], client) == []

    def test_equality(self):
        a = MusicHistoryTab(date=self.date)
        b = MusicHistoryTab(date='2025-02-01')
        c = MusicHistoryTab(date=self.date)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
