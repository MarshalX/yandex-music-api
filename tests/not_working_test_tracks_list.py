import pytest

from yandex_music import TracksList


@pytest.fixture(scope='class')
def tracks_list(tracks):
    return TracksList(TestTracksList.uid, TestTracksList.revision, tracks)


class TestTracksList:
    uid = None
    revision = None

    def test_expected_values(self, tracks_list, tracks):
        assert tracks_list.uid == self.uid
        assert tracks_list.revision == self.revision
        assert tracks_list.tracks == tracks

    def test_de_json_required(self, client, tracks):
        json_dict = {'uid': self.uid, 'revision': self.revision, 'tracks': tracks}
        tracks_list = TracksList.de_json(json_dict, client)

        assert tracks_list.uid == self.uid
        assert tracks_list.revision == self.revision
        assert tracks_list.tracks == tracks

    def test_de_json_all(self, client, tracks):
        json_dict = {'uid': self.uid, 'revision': self.revision, 'tracks': tracks}
        tracks_list = TracksList.de_json(json_dict, client)

        assert tracks_list.uid == self.uid
        assert tracks_list.revision == self.revision
        assert tracks_list.tracks == tracks

    def test_equality(self):
        pass
