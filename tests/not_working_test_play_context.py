import pytest

from yandex_music import PlayContext


@pytest.fixture(scope='class')
def play_context(tracks):
    return PlayContext(TestPlayContext.client_, TestPlayContext.context, TestPlayContext.context_item, tracks)


class TestPlayContext:
    client_ = None
    context = None
    context_item = None

    def test_expected_values(self, play_context, tracks):
        assert play_context.client_ == self.client_
        assert play_context.context == self.context
        assert play_context.context_item == self.context_item
        assert play_context.tracks == tracks

    def test_de_json_required(self, client, tracks):
        json_dict = {'client_': self.client_, 'context': self.context, 'context_item': self.context_item,
                     'tracks': tracks}
        play_context = PlayContext.de_json(json_dict, client)

        assert play_context.client_ == self.client_
        assert play_context.context == self.context
        assert play_context.context_item == self.context_item
        assert play_context.tracks == tracks

    def test_de_json_all(self, client, tracks):
        json_dict = {'client_': self.client_, 'context': self.context, 'context_item': self.context_item,
                     'tracks': tracks}
        play_context = PlayContext.de_json(json_dict, client)

        assert play_context.client_ == self.client_
        assert play_context.context == self.context
        assert play_context.context_item == self.context_item
        assert play_context.tracks == tracks

    def test_equality(self):
        pass
