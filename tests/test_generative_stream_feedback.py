from yandex_music import GenerativeStreamFeedback


class TestGenerativeStreamFeedback:
    reload_stream = False
    not_paused = True

    def test_expected_values(self, generative_stream_feedback):
        assert generative_stream_feedback.reload_stream == self.reload_stream
        assert generative_stream_feedback.not_paused == self.not_paused

    def test_de_json_none(self, client):
        assert GenerativeStreamFeedback.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'reload_stream': self.reload_stream, 'not_paused': self.not_paused}
        generative_stream_feedback = GenerativeStreamFeedback.de_json(json_dict, client)

        assert generative_stream_feedback.reload_stream == self.reload_stream
        assert generative_stream_feedback.not_paused == self.not_paused

    def test_equality(self):
        a = GenerativeStreamFeedback(self.reload_stream, self.not_paused)
        b = GenerativeStreamFeedback(self.reload_stream, False)
        c = GenerativeStreamFeedback(self.reload_stream, self.not_paused)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
