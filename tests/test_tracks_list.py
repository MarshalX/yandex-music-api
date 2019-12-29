import pytest

from yandex_music import TracksList


@pytest.fixture(scope='class')
def tracks_list(track_short):
    return TracksList(TestTracksList.uid, TestTracksList.revision, [track_short])


class TestTracksList:
    uid = None
    revision = None

    def test_expected_values(self, tracks_list, track_short):
        assert tracks_list.uid == self.uid
        assert tracks_list.revision == self.revision
        assert tracks_list.tracks == [track_short]

    def test_de_json_none(self, client):
        assert TracksList.de_json({}, client) is None

    def test_de_json_required(self, client, track_short):
        json_dict = {'uid': self.uid, 'revision': self.revision, 'tracks': [track_short.to_dict()]}
        tracks_list = TracksList.de_json(json_dict, client)

        assert tracks_list.uid == self.uid
        assert tracks_list.revision == self.revision
        assert tracks_list.tracks == [track_short]

    def test_de_json_all(self, client, track_short):
        json_dict = {'uid': self.uid, 'revision': self.revision, 'tracks': [track_short.to_dict()]}
        tracks_list = TracksList.de_json(json_dict, client)

        assert tracks_list.uid == self.uid
        assert tracks_list.revision == self.revision
        assert tracks_list.tracks == [track_short]

    def test_equality(self, track_short):
        a = TracksList(self.uid, self.revision, [track_short])
        b = TracksList(123, self.revision, [track_short])
        c = TracksList(self.uid, 10, [track_short])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
