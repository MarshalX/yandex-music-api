from typing import Dict

import pytest

from yandex_music import Client, Context, JSONType, QueueItem


@pytest.fixture(scope='class')
def queue_item(context: Context) -> QueueItem:
    return QueueItem(TestQueueItem.id_, context, TestQueueItem.modified)


class TestQueueItem:
    id_ = '503646255:69814820'
    modified = '2020-06-20T13:29:09Z'

    def test_expected_values(self, queue_item: QueueItem, context: Context) -> None:
        assert queue_item.id == self.id_
        assert queue_item.context == context
        assert queue_item.modified == self.modified

    def test_de_json_none(self, client: Client) -> None:
        assert QueueItem.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert QueueItem.de_list([], client) == []

    def test_de_json_required(self, client: Client, context: Context) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id_, 'context': context.to_dict(), 'modified': self.modified}
        queue_item = QueueItem.de_json(json_dict, client)
        assert queue_item is not None

        assert queue_item.id == self.id_
        assert queue_item.context == context
        assert queue_item.modified == self.modified

    def test_de_json_all(self, client: Client, context: Context) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id_, 'context': context.to_dict(), 'modified': self.modified}
        queue_item = QueueItem.de_json(json_dict, client)
        assert queue_item is not None

        assert queue_item.id == self.id_
        assert queue_item.context == context
        assert queue_item.modified == self.modified

    def test_equality(self, context: Context) -> None:
        a = QueueItem(self.id_, context, self.modified)
        b = QueueItem('', context, self.modified)
        c = QueueItem(self.id_, context, self.modified)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
