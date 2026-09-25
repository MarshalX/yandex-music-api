from yandex_music import RotorSessionTracks


class TestRotorSessionTracks:
    batch_id = 'fake-batch-id.2'
    pumpkin = False
    terminated = False
    unknown_session = False
    offline_recommender_data = [1]

    def test_expected_values(self, rotor_session_tracks, sequence):
        assert rotor_session_tracks.batch_id == self.batch_id
        assert rotor_session_tracks.pumpkin == self.pumpkin
        assert rotor_session_tracks.sequence == [sequence]
        assert rotor_session_tracks.terminated == self.terminated
        assert rotor_session_tracks.unknown_session == self.unknown_session
        assert rotor_session_tracks.offline_recommender_data == self.offline_recommender_data

    def test_de_json_none(self, client):
        assert RotorSessionTracks.de_json({}, client) is None

    def test_de_json_all(self, client, sequence):
        json_dict = {
            'batchId': self.batch_id,
            'pumpkin': self.pumpkin,
            'sequence': [sequence.to_dict()],
            'terminated': self.terminated,
            'unknownSession': self.unknown_session,
            'offlineRecommenderData': self.offline_recommender_data,
        }
        rotor_session_tracks = RotorSessionTracks.de_json(json_dict, client)

        assert rotor_session_tracks.batch_id == self.batch_id
        assert rotor_session_tracks.pumpkin == self.pumpkin
        assert rotor_session_tracks.sequence == [sequence]
        assert rotor_session_tracks.terminated == self.terminated
        assert rotor_session_tracks.unknown_session == self.unknown_session
        assert rotor_session_tracks.offline_recommender_data == self.offline_recommender_data

    def test_equality(self, sequence):
        a = RotorSessionTracks(self.batch_id, sequence=[sequence])
        b = RotorSessionTracks('other-batch-id', sequence=[sequence])
        c = RotorSessionTracks(self.batch_id, sequence=[sequence])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
