from yandex_music import SessionFeedbacks


class TestSessionFeedbacks:
    session_id = 'fake-radio-session-id'

    def test_expected_values(self, session_feedbacks, session_feedback):
        assert session_feedbacks.session_id == self.session_id
        assert session_feedbacks.feedbacks == [session_feedback]

    def test_de_json_none(self, client):
        assert SessionFeedbacks.de_json({}, client) is None

    def test_de_json_all(self, client, session_feedback):
        json_dict = {'sessionId': self.session_id, 'feedbacks': [session_feedback.to_dict()]}
        session_feedbacks = SessionFeedbacks.de_json(json_dict, client)

        assert session_feedbacks.session_id == self.session_id
        assert session_feedbacks.feedbacks == [session_feedback]

    def test_to_dict_for_request(self, session_feedbacks, session_feedback):
        assert session_feedbacks.to_dict(for_request=True) == {
            'sessionId': self.session_id,
            'feedbacks': [session_feedback.to_dict(for_request=True)],
        }

    def test_equality(self, session_feedback):
        a = SessionFeedbacks(self.session_id, [session_feedback])
        b = SessionFeedbacks('other-session-id', [session_feedback])
        c = SessionFeedbacks(self.session_id, [session_feedback])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
