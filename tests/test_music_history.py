from yandex_music import HistoryTab, HistoryTabContext, HistoryTabItem, HistoryTrack, TrackContextData, TrackItemId


class TestHistoryTab:
    date = '2026-01-23'

    def test_expected_values(self, history_tab, history_tab_item):
        assert history_tab.date == self.date
        assert history_tab.items == [history_tab_item]

    def test_de_json_none(self, client):
        assert HistoryTab.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert HistoryTab.de_list([], client) == []

    def test_de_json_required(self, client, history_tab_item):
        json_dict = {'date': self.date, 'items': [history_tab_item.to_dict()]}
        history_tab = HistoryTab.de_json(json_dict, client)

        assert history_tab.date == self.date
        assert history_tab.items == [history_tab_item]

    def test_de_json_all(self, client, history_tab_item):
        json_dict = {'date': self.date, 'items': [history_tab_item.to_dict()]}
        history_tab = HistoryTab.de_json(json_dict, client)

        assert history_tab.date == self.date
        assert history_tab.items == [history_tab_item]

    def test_equality(self, history_tab_item):
        a = HistoryTab(self.date, [history_tab_item])
        b = HistoryTab('2026-01-20', [history_tab_item])
        c = HistoryTab(self.date, [])
        d = HistoryTab(self.date, [history_tab_item])

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d


class TestHistoryTabItem:
    def test_expected_values(self, history_tab_item, history_tab_context, history_track):
        assert history_tab_item.context == history_tab_context
        assert history_tab_item.tracks == [history_track]

    def test_de_json_none(self, client):
        assert HistoryTabItem.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert HistoryTabItem.de_list([], client) == []

    def test_de_json_required(self, client, history_tab_context, history_track):
        json_dict = {'context': history_tab_context.to_dict(), 'tracks': [history_track.to_dict()]}
        history_tab_item = HistoryTabItem.de_json(json_dict, client)

        assert history_tab_item.context == history_tab_context
        assert history_tab_item.tracks == [history_track]

    def test_de_json_all(self, client, history_tab_context, history_track):
        json_dict = {'context': history_tab_context.to_dict(), 'tracks': [history_track.to_dict()]}
        history_tab_item = HistoryTabItem.de_json(json_dict, client)

        assert history_tab_item.context == history_tab_context
        assert history_tab_item.tracks == [history_track]

    def test_equality(self, history_tab_context, history_track):
        a = HistoryTabItem(history_tab_context, [history_track])
        b = HistoryTabItem(history_tab_context, [])
        c = HistoryTabItem(history_tab_context, [history_track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c


class TestHistoryTabContext:
    type = 'search'

    def test_expected_values(self, history_tab_context):
        assert history_tab_context.type == self.type
        assert history_tab_context.data is None

    def test_de_json_none(self, client):
        assert HistoryTabContext.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'type': self.type}
        history_tab_context = HistoryTabContext.de_json(json_dict, client)

        assert history_tab_context.type == self.type
        assert history_tab_context.data is None

    def test_de_json_all(self, client):
        json_dict = {'type': self.type}
        history_tab_context = HistoryTabContext.de_json(json_dict, client)

        assert history_tab_context.type == self.type
        assert history_tab_context.data is None

    def test_equality(self):
        a = HistoryTabContext(self.type)
        b = HistoryTabContext('wave')
        c = HistoryTabContext(self.type)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c


class TestHistoryTrack:
    type = 'track'

    def test_expected_values(self, history_track, track_context_data):
        assert history_track.type == self.type
        assert history_track.data == track_context_data

    def test_de_json_none(self, client):
        assert HistoryTrack.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert HistoryTrack.de_list([], client) == []

    def test_de_json_required(self, client, track_context_data):
        json_dict = {'type': self.type, 'data': track_context_data.to_dict()}
        history_track = HistoryTrack.de_json(json_dict, client)

        assert history_track.type == self.type
        assert history_track.data == track_context_data

    def test_de_json_all(self, client, track_context_data):
        json_dict = {'type': self.type, 'data': track_context_data.to_dict()}
        history_track = HistoryTrack.de_json(json_dict, client)

        assert history_track.type == self.type
        assert history_track.data == track_context_data

    def test_equality(self, track_context_data):
        a = HistoryTrack(self.type, track_context_data)
        b = HistoryTrack('other', track_context_data)
        c = HistoryTrack(self.type, track_context_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c


class TestTrackContextData:
    def test_expected_values(self, track_context_data, track_item_id, track):
        assert track_context_data.item_id == track_item_id
        assert track_context_data.full_model == track

    def test_de_json_none(self, client):
        assert TrackContextData.de_json({}, client) is None

    def test_de_json_required(self, client, track_item_id, track):
        json_dict = {'item_id': track_item_id.to_dict(), 'full_model': track.to_dict()}
        track_context_data = TrackContextData.de_json(json_dict, client)

        assert track_context_data.item_id == track_item_id
        assert track_context_data.full_model == track

    def test_de_json_all(self, client, track_item_id, track):
        json_dict = {'item_id': track_item_id.to_dict(), 'full_model': track.to_dict()}
        track_context_data = TrackContextData.de_json(json_dict, client)

        assert track_context_data.item_id == track_item_id
        assert track_context_data.full_model == track

    def test_equality(self, track_item_id, track):
        a = TrackContextData(track_item_id, track)
        b = TrackContextData(track_item_id, None)
        c = TrackContextData(track_item_id, track)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c


class TestTrackItemId:
    track_id = '12345678'
    album_id = '11111111'

    def test_expected_values(self, track_item_id):
        assert track_item_id.track_id == self.track_id
        assert track_item_id.album_id == self.album_id

    def test_de_json_none(self, client):
        assert TrackItemId.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'track_id': self.track_id, 'album_id': self.album_id}
        track_item_id = TrackItemId.de_json(json_dict, client)

        assert track_item_id.track_id == self.track_id
        assert track_item_id.album_id == self.album_id

    def test_de_json_all(self, client):
        json_dict = {'track_id': self.track_id, 'album_id': self.album_id}
        track_item_id = TrackItemId.de_json(json_dict, client)

        assert track_item_id.track_id == self.track_id
        assert track_item_id.album_id == self.album_id

    def test_equality(self):
        a = TrackItemId(self.track_id, self.album_id)
        b = TrackItemId('87654321', self.album_id)
        c = TrackItemId(self.track_id, '22222222')
        d = TrackItemId(self.track_id, self.album_id)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
