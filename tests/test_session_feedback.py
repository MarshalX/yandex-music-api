from yandex_music import SessionFeedback


class TestSessionFeedback:
    batch_id = 'fake-batch-id.3'
    from_ = 'radio-mobile-user-onyourwave'

    def test_expected_values(self, session_feedback, session_event):
        assert session_feedback.event == session_event
        assert session_feedback.batch_id == self.batch_id
        assert session_feedback.from_ == self.from_

    def test_de_json_none(self, client):
        assert SessionFeedback.de_json({}, client) is None

    def test_de_json_all(self, client, session_event):
        json_dict = {'event': session_event.to_dict(), 'batchId': self.batch_id, 'from': self.from_}
        session_feedback = SessionFeedback.de_json(json_dict, client)

        assert session_feedback.event == session_event
        assert session_feedback.batch_id == self.batch_id
        assert session_feedback.from_ == self.from_

    def test_to_dict_for_request(self, session_feedback, session_event):
        assert session_feedback.to_dict(for_request=True) == {
            'event': session_event.to_dict(for_request=True),
            'batchId': self.batch_id,
            'from': self.from_,
        }

    def test_equality(self, session_event):
        a = SessionFeedback(session_event, self.batch_id)
        b = SessionFeedback(session_event, 'other-batch-id')
        c = SessionFeedback(session_event, self.batch_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
