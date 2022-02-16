import pytest

from yandex_music import QueueItem


@pytest.fixture(scope='class')
def queue_item(context):
    return QueueItem(TestQueueItem.id_, context, TestQueueItem.modified)


class TestQueueItem:
    id_ = '503646255:69814820'
    modified = '2020-06-20T13:29:09Z'

    def test_expected_values(self, queue_item, context):
        assert queue_item.id == self.id_
        assert queue_item.context == context
        assert queue_item.modified == self.modified

    def test_de_json_none(self, client):
        assert QueueItem.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert QueueItem.de_list({}, client) == []

    def test_de_json_required(self, client, context):
        json_dict = {'id': self.id_, 'context': context.to_dict(), 'modified': self.modified}
        queue_item = QueueItem.de_json(json_dict, client)

        assert queue_item.id == self.id_
        assert queue_item.context == context
        assert queue_item.modified == self.modified

    def test_de_json_all(self, client, context):
        json_dict = {'id': self.id_, 'context': context.to_dict(), 'modified': self.modified}
        queue_item = QueueItem.de_json(json_dict, client)

        assert queue_item.id == self.id_
        assert queue_item.context == context
        assert queue_item.modified == self.modified

    def test_equality(self, context):
        a = QueueItem(self.id_, context, self.modified)
        b = QueueItem('', context, self.modified)
        c = QueueItem(self.id_, context, self.modified)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
