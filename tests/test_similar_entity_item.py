from typing import Dict

from yandex_music import Client, JSONType, SimilarEntityData, SimilarEntityItem


class TestSimilarEntityItem:
    type = 'wave_agent_item'

    def test_expected_values(
        self, similar_entity_item: SimilarEntityItem, similar_entity_data: SimilarEntityData
    ) -> None:
        assert similar_entity_item.type == self.type
        assert similar_entity_item.data == similar_entity_data

    def test_de_json_none(self, client: Client) -> None:
        assert SimilarEntityItem.de_json({}, client) is None

    def test_de_json_all(self, client: Client, similar_entity_data: SimilarEntityData) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'data': similar_entity_data.to_dict(),
        }
        item = SimilarEntityItem.de_json(json_dict, client)
        assert item is not None

        assert item.type == self.type
        assert item.data == similar_entity_data

    def test_de_list(self, client: Client, similar_entity_data: SimilarEntityData) -> None:
        json_list = [
            {
                'type': self.type,
                'data': similar_entity_data.to_dict(),
            },
        ]
        items = SimilarEntityItem.de_list(json_list, client)

        assert len(items) == 1
        assert items[0].type == self.type

    def test_equality(self, similar_entity_data: SimilarEntityData) -> None:
        a = SimilarEntityItem(type=self.type, data=similar_entity_data)
        b = SimilarEntityItem(type='other', data=similar_entity_data)
        c = SimilarEntityItem(type=self.type, data=similar_entity_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
