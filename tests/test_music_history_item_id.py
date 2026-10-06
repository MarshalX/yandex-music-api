from typing import Dict

from yandex_music import Client, JSONType, MusicHistoryItemId


class TestMusicHistoryItemId:
    id = '12345'
    track_id = '67890'
    album_id = '54321'
    uid = 100500
    kind = 3
    seeds = ['user:onyourwave']

    def test_expected_value(self, music_history_item_id: MusicHistoryItemId) -> None:
        assert music_history_item_id.id == self.id
        assert music_history_item_id.track_id == self.track_id
        assert music_history_item_id.album_id == self.album_id

    def test_de_json_none(self, client: Client) -> None:
        assert MusicHistoryItemId.de_json({}, client) is None

    def test_de_json_track(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'trackId': self.track_id,
            'albumId': self.album_id,
        }
        item_id = MusicHistoryItemId.de_json(json_dict, client)
        assert item_id is not None
        assert item_id.track_id == self.track_id
        assert item_id.album_id == self.album_id

    def test_de_json_album(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id}
        item_id = MusicHistoryItemId.de_json(json_dict, client)
        assert item_id is not None
        assert item_id.id == self.id

    def test_de_json_playlist(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'uid': self.uid, 'kind': self.kind}
        item_id = MusicHistoryItemId.de_json(json_dict, client)
        assert item_id is not None
        assert item_id.uid == self.uid
        assert item_id.kind == self.kind

    def test_de_json_wave(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'seeds': self.seeds}
        item_id = MusicHistoryItemId.de_json(json_dict, client)
        assert item_id is not None
        assert item_id.seeds == self.seeds

    def test_equality(self) -> None:
        a = MusicHistoryItemId(id=self.id, track_id=self.track_id, album_id=self.album_id)
        b = MusicHistoryItemId(id='other')
        c = MusicHistoryItemId(id=self.id, track_id=self.track_id, album_id=self.album_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
