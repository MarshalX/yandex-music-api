import pytest

from yandex_music import Block


@pytest.fixture(scope='class')
def block_with_entity_and_data(block_entity, data):
    return (
        Block(
            TestBlock.id,
            TestBlock.type,
            TestBlock.type_for_from,
            TestBlock.title,
            [block_entity],
            TestBlock.description,
            data,
        ),
        block_entity,
        data,
    )


class TestBlock:
    id = 'ObsM5DkU'
    type = 'personal-playlists'
    type_for_from = 'personal-playlists'
    title = 'Собрано на основе ваших предпочтений'
    description = None

    def test_expected_values(self, block_with_entity_and_data):
        block, block_entity, data = block_with_entity_and_data

        assert block.id == self.id
        assert block.type == self.type
        assert block.type_for_from == self.type_for_from
        assert block.title == self.title
        assert block.entities == [block_entity]
        assert block.description == self.description
        assert block.data == data

    def test_de_json_none(self, client):
        assert Block.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Block.de_list({}, client) == []

    def test_de_json_required(self, client, block_entity):
        json_dict = {
            'id': self.id,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'entities': [block_entity.to_dict()],
        }
        block = Block.de_json(json_dict, client)

        assert block.id == self.id
        assert block.type == self.type
        assert block.type_for_from == self.type_for_from
        assert block.title == self.title
        assert block.entities == [block_entity]

    def test_de_json_all(self, client, block_entity, data_with_type):
        data, type_ = data_with_type

        json_dict = {
            'id': self.id,
            'type': type_,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'entities': [block_entity.to_dict()],
            'description': self.description,
            'data': data.to_dict(),
        }
        block = Block.de_json(json_dict, client)

        assert block.id == self.id
        assert block.type == type_
        assert block.type_for_from == self.type_for_from
        assert block.title == self.title
        assert block.entities == [block_entity]
        assert block.description == self.description
        assert block.data == data

    def test_equality(self, block_entity):
        a = Block(self.id, self.type, self.type_for_from, self.title, [block_entity])
        b = Block('', self.type, self.type_for_from, self.title, [])
        c = Block(self.id, self.type, self.type_for_from, self.title, [block_entity])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
