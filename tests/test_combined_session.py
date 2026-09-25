from yandex_music import CombinedSession


class TestCombinedSession:
    session_id = 'fake-combined-session-id'
    batch_id = 'fake-batch-id.4'
    pumpkin = False

    def test_expected_values(self, combined_session, combined_session_item):
        assert combined_session.session_id == self.session_id
        assert combined_session.batch_id == self.batch_id
        assert combined_session.pumpkin == self.pumpkin
        assert combined_session.list == [combined_session_item]

    def test_de_json_none(self, client):
        assert CombinedSession.de_json({}, client) is None

    def test_de_json_all(self, client, combined_session_item):
        json_dict = {
            'sessionId': self.session_id,
            'batchId': self.batch_id,
            'pumpkin': self.pumpkin,
            'list': [combined_session_item.to_dict()],
        }
        combined_session = CombinedSession.de_json(json_dict, client)

        assert combined_session.session_id == self.session_id
        assert combined_session.batch_id == self.batch_id
        assert combined_session.pumpkin == self.pumpkin
        assert combined_session.list == [combined_session_item]

    def test_equality(self):
        a = CombinedSession(self.session_id, self.batch_id)
        b = CombinedSession('other-session-id', self.batch_id)
        c = CombinedSession(self.session_id, self.batch_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
