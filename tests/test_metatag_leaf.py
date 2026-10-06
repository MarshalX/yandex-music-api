from typing import Dict

from yandex_music import Client, JSONType, MetatagLeaf


class TestMetatagLeaf:
    tag = 'Весенняя музыка'
    title = 'Весеннее'

    def test_expected_values(self, metatag_leaf: MetatagLeaf, metatag_leaf_nested: MetatagLeaf) -> None:
        assert metatag_leaf.tag == self.tag
        assert metatag_leaf.title == self.title
        assert metatag_leaf.leaves == [metatag_leaf_nested]

    def test_de_json_none(self, client: Client) -> None:
        assert MetatagLeaf.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'tag': self.tag, 'title': self.title}
        metatag_leaf = MetatagLeaf.de_json(json_dict, client)
        assert metatag_leaf is not None

        assert metatag_leaf.tag == self.tag
        assert metatag_leaf.title == self.title
        assert metatag_leaf.leaves == []

    def test_de_json_all(self, client: Client, metatag_leaf_nested: MetatagLeaf) -> None:
        json_dict: Dict[str, JSONType] = {
            'tag': self.tag,
            'title': self.title,
            'leaves': [metatag_leaf_nested.to_dict()],
        }
        metatag_leaf = MetatagLeaf.de_json(json_dict, client)
        assert metatag_leaf is not None

        assert metatag_leaf.tag == self.tag
        assert metatag_leaf.title == self.title
        assert metatag_leaf.leaves == [metatag_leaf_nested]

    def test_equality(self, metatag_leaf_nested: MetatagLeaf) -> None:
        a = MetatagLeaf(tag=self.tag, title=self.title, leaves=[metatag_leaf_nested])
        b = MetatagLeaf(tag='other', title=self.title, leaves=[metatag_leaf_nested])
        c = MetatagLeaf(tag=self.tag, title=self.title, leaves=[metatag_leaf_nested])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
