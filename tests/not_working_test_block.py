import pytest

from yandex_music import Block


@pytest.fixture(scope='class')
def block(type, entities, data):
    return Block(TestBlock.id, type, TestBlock.type_for_from, TestBlock.title, entities, TestBlock.description, data)


class TestBlock:
    type = None
    type_for_from = None
    title = None

    def test_expected_values(self, block, id, entities, description, data):
        assert block.id == id
        assert block.type == self.type
        assert block.type_for_from == self.type_for_from
        assert block.title == self.title
        assert block.entities == entities
        assert block.description == description
        assert block.data == data

    def test_de_json_required(self, client, id, entities):
        json_dict = {'id': id, 'type': self.type, 'type_for_from': self.type_for_from, 'title': self.title,
                     'entities': entities}
        block = Block.de_json(json_dict, client)

        assert block.id == id
        assert block.type == self.type
        assert block.type_for_from == self.type_for_from
        assert block.title == self.title
        assert block.entities == entities

    def test_de_json_all(self, client, id, entities, description, data):
        json_dict = {'id': id, 'type': self.type, 'type_for_from': self.type_for_from, 'title': self.title,
                     'entities': entities, 'description': description, 'data': data}
        block = Block.de_json(json_dict, client)

        assert block.id == id
        assert block.type == self.type
        assert block.type_for_from == self.type_for_from
        assert block.title == self.title
        assert block.entities == entities
        assert block.description == description
        assert block.data == data

    def test_equality(self):
        pass
