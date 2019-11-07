import pytest

from yandex_music import PlaylistId


@pytest.fixture(scope='class')
def playlist_id():
    return PlaylistId(TestPlaylistId.uid, TestPlaylistId.kind)


class TestPlaylistId:
    uid = None
    kind = None

    def test_expected_values(self, playlist_id):
        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_de_json_required(self, client):
        json_dict = {'uid': self.uid, 'kind': self.kind}
        playlist_id = PlaylistId.de_json(json_dict, client)

        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_de_json_all(self, client):
        json_dict = {'uid': self.uid, 'kind': self.kind}
        playlist_id = PlaylistId.de_json(json_dict, client)

        assert playlist_id.uid == self.uid
        assert playlist_id.kind == self.kind

    def test_equality(self):
        pass
