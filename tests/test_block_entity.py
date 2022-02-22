import pytest

from yandex_music import BlockEntity


@pytest.fixture(scope='class', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity_data_with_type(request, results, types):
    return results[request.param], types[request.param]


@pytest.fixture(scope='class', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity_with_data_and_type(request, results, types):
    return (
        BlockEntity(TestBlockEntity.id, types[request.param], results[request.param]),
        results[request.param],
        types[request.param],
    )


class TestBlockEntity:
    id = 'lze0IVH4'
    type = 'personal-playlist'

    def test_expected_values(self, block_entity_with_data_and_type):
        block_entity, data, type_ = block_entity_with_data_and_type

        assert block_entity.id == self.id
        assert block_entity.type == type_
        assert block_entity.data == data

    def test_de_list_none(self, client):
        assert BlockEntity.de_list({}, client) == []

    def test_de_json_none(self, client):
        assert BlockEntity.de_json({}, client) is None

    def test_de_json_required(self, client, block_entity_data_with_type):
        data, type_ = block_entity_data_with_type

        json_dict = {'id': self.id, 'type': type_, 'data': data.to_dict()}
        block_entity = BlockEntity.de_json(json_dict, client)

        assert block_entity.id == self.id
        assert block_entity.type == type_
        assert block_entity.data == data

    def test_de_json_all(self, client, block_entity_data_with_type):
        data, type_ = block_entity_data_with_type

        json_dict = {'id': self.id, 'type': type_, 'data': data.to_dict()}
        block_entity = BlockEntity.de_json(json_dict, client)

        assert block_entity.id == self.id
        assert block_entity.type == type_
        assert block_entity.data == data

    def test_equality(self, block_entity_data_with_type):
        data, type = block_entity_data_with_type

        a = BlockEntity(self.id, type, data)
        b = BlockEntity(self.id, '', data)
        c = BlockEntity('', type, data)
        d = BlockEntity(self.id, type, data)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
