from yandex_music import CombinedSessionQueueItem


class TestCombinedSessionQueueItem:
    type = 'CLIP'
    id = '100500'

    def test_expected_values(self, combined_session_queue_item):
        assert combined_session_queue_item.type == self.type
        assert combined_session_queue_item.id == self.id

    def test_de_json_none(self, client):
        assert CombinedSessionQueueItem.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'type': self.type, 'id': self.id}
        combined_session_queue_item = CombinedSessionQueueItem.de_json(json_dict, client)

        assert combined_session_queue_item.type == self.type
        assert combined_session_queue_item.id == self.id

    def test_to_dict_for_request(self, combined_session_queue_item):
        assert combined_session_queue_item.to_dict(for_request=True) == {'type': self.type, 'id': self.id}

    def test_equality(self):
        a = CombinedSessionQueueItem(self.type, self.id)
        b = CombinedSessionQueueItem('TRACK', self.id)
        c = CombinedSessionQueueItem(self.type, self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
