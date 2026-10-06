from typing import Dict

from yandex_music import Client, JSONType, PlaylistId


class TestPlaylistId:
    uid = 460142547
    kind = 5332052

    def test_expected_values(self, playlist_id: PlaylistId) -> None:
        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_de_json_none(self, client: Client) -> None:
        assert PlaylistId.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert PlaylistId.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'uid': self.uid, 'kind': self.kind}
        playlist_id = PlaylistId.de_json(json_dict, client)
        assert playlist_id is not None

        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'uid': self.uid, 'kind': self.kind}
        playlist_id = PlaylistId.de_json(json_dict, client)
        assert playlist_id is not None

        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_equality(self) -> None:
        a = PlaylistId(self.uid, self.kind)
        b = PlaylistId(self.uid, 10)
        c = PlaylistId(10, self.kind)
        d = PlaylistId(self.uid, self.kind)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
