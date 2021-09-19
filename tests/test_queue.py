import pytest

from yandex_music import Queue


@pytest.fixture(scope='session')
def queue(context, track_id):
    return Queue(context, [track_id], TestQueue.current_index, TestQueue.modified, TestQueue.id_, TestQueue.from_)


class TestQueue:
    current_index = 1
    modified = '2020-06-20T13:29:09Z'
    id_ = '5eee0f257c28205469d8433c'
    from_ = 'mobile-home-playlist_of_the_day-default'

    def test_expected_values(self, queue, context, track_id):
        assert queue.context == context
        assert queue.tracks == [track_id]
        assert queue.current_index == self.current_index
        assert queue.modified == self.modified
        assert queue.id == self.id_
        assert queue.from_ == self.from_

    def test_de_json_none(self, client):
        assert Queue.de_json({}, client) is None

    def test_de_json_required(self, client, context, track_id):
        json_dict = {
            'context': context.to_dict(),
            'modified': self.modified,
            'current_index': self.current_index,
            'tracks': [track_id.to_dict()],
        }
        queue = Queue.de_json(json_dict, client)

        assert queue.context == context
        assert queue.tracks == [track_id]
        assert queue.current_index == self.current_index
        assert queue.modified == self.modified

    def test_de_json_all(self, client, context, track_id):
        json_dict = {
            'context': context.to_dict(),
            'modified': self.modified,
            'id': self.id_,
            'from_': self.from_,
            'current_index': self.current_index,
            'tracks': [track_id.to_dict()],
        }
        queue = Queue.de_json(json_dict, client)

        assert queue.context == context
        assert queue.tracks == [track_id]
        assert queue.current_index == self.current_index
        assert queue.modified == self.modified
        assert queue.id == self.id_
        assert queue.from_ == self.from_

    def test_equality(self, context, track_id):
        a = Queue(context, [track_id], self.current_index, self.modified)
        b = Queue(context, [], self.current_index, self.modified)
        c = Queue(context, [track_id], self.current_index, self.modified)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
