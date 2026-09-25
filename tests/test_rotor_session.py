from yandex_music import RotorSession


class TestRotorSession:
    radio_session_id = 'fake-radio-session-id'
    batch_id = 'fake-batch-id.1'
    pumpkin = False
    terminated = False
    offline_recommender_data = [1, 2, 3]
    interactive = True

    def test_expected_values(self, rotor_session, sequence, rotor_seed, wave):
        assert rotor_session.radio_session_id == self.radio_session_id
        assert rotor_session.batch_id == self.batch_id
        assert rotor_session.pumpkin == self.pumpkin
        assert rotor_session.sequence == [sequence]
        assert rotor_session.accepted_seeds == [rotor_seed]
        assert rotor_session.description_seed == rotor_seed
        assert rotor_session.terminated == self.terminated
        assert rotor_session.wave == wave
        assert rotor_session.offline_recommender_data == self.offline_recommender_data
        assert rotor_session.interactive == self.interactive

    def test_de_json_none(self, client):
        assert RotorSession.de_json({}, client) is None

    def test_de_json_all(self, client, sequence, rotor_seed, wave):
        json_dict = {
            'radioSessionId': self.radio_session_id,
            'batchId': self.batch_id,
            'pumpkin': self.pumpkin,
            'sequence': [sequence.to_dict()],
            'acceptedSeeds': [rotor_seed.to_dict()],
            'descriptionSeed': rotor_seed.to_dict(),
            'terminated': self.terminated,
            'wave': wave.to_dict(),
            'offlineRecommenderData': self.offline_recommender_data,
            'interactive': self.interactive,
        }
        rotor_session = RotorSession.de_json(json_dict, client)

        assert rotor_session.radio_session_id == self.radio_session_id
        assert rotor_session.batch_id == self.batch_id
        assert rotor_session.pumpkin == self.pumpkin
        assert rotor_session.sequence == [sequence]
        assert rotor_session.accepted_seeds == [rotor_seed]
        assert rotor_session.description_seed == rotor_seed
        assert rotor_session.terminated == self.terminated
        assert rotor_session.wave == wave
        assert rotor_session.offline_recommender_data == self.offline_recommender_data
        assert rotor_session.interactive == self.interactive

    def test_equality(self):
        a = RotorSession(self.radio_session_id, self.batch_id)
        b = RotorSession('other-session-id', self.batch_id)
        c = RotorSession(self.radio_session_id, self.batch_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
