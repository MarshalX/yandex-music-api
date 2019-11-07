import pytest

from yandex_music import BlockEntity


@pytest.fixture(scope='class')
def block_entity(type, data):
    return BlockEntity(TestBlockEntity.id, type, data)


class TestBlockEntity:
    type = None

    def test_expected_values(self, block_entity, id, data):
        assert block_entity.id == id
        assert block_entity.type == self.type
        assert block_entity.data == data

    def test_de_json_required(self, client, id, data):
        json_dict = {'id': id, 'type': self.type, 'data': data}
        block_entity = BlockEntity.de_json(json_dict, client)

        assert block_entity.id == id
        assert block_entity.type == self.type
        assert block_entity.data == data

    def test_de_json_all(self, client, id, data):
        json_dict = {'id': id, 'type': self.type, 'data': data}
        block_entity = BlockEntity.de_json(json_dict, client)

        assert block_entity.id == id
        assert block_entity.type == self.type
        assert block_entity.data == data

    def test_equality(self):
        pass
