from yandex_music import PlayContext


class TestPlayContext:
    client_ = 'android'
    context = 'playlist'
    context_item = '503646255:69814820'

    def test_expected_values(self, play_context, track_short_old):
        assert play_context.client_ == self.client_
        assert play_context.context == self.context
        assert play_context.context_item == self.context_item
        assert play_context.tracks == [track_short_old]

    def test_de_json_none(self, client):
        assert PlayContext.de_json({}, client) is None

    def test_de_json_required(self, client, track_short_old):
        json_dict = {
            'client_': self.client_,
            'context': self.context,
            'context_item': self.context_item,
            'tracks': [track_short_old.to_dict()],
        }
        play_context = PlayContext.de_json(json_dict, client)

        assert play_context.client_ == self.client_
        assert play_context.context == self.context
        assert play_context.context_item == self.context_item
        assert play_context.tracks == [track_short_old]

    def test_de_json_all(self, client, track_short_old):
        json_dict = {
            'client_': self.client_,
            'context': self.context,
            'context_item': self.context_item,
            'tracks': [track_short_old.to_dict()],
        }
        play_context = PlayContext.de_json(json_dict, client)

        assert play_context.client_ == self.client_
        assert play_context.context == self.context
        assert play_context.context_item == self.context_item
        assert play_context.tracks == [track_short_old]

    def test_equality(self, track_short_old):
        a = PlayContext(self.client_, self.context, self.context_item, [track_short_old])
        b = PlayContext('', self.context, self.context_item, [])
        c = PlayContext(self.client_, self.context, self.context_item, [track_short_old])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
