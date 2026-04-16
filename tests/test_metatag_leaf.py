from yandex_music import MetatagLeaf


class TestMetatagLeaf:
    tag = 'Весенняя музыка'
    title = 'Весеннее'

    def test_expected_values(self, metatag_leaf, metatag_leaf_nested):
        assert metatag_leaf.tag == self.tag
        assert metatag_leaf.title == self.title
        assert metatag_leaf.leaves == [metatag_leaf_nested]

    def test_de_json_none(self, client):
        assert MetatagLeaf.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'tag': self.tag, 'title': self.title}
        metatag_leaf = MetatagLeaf.de_json(json_dict, client)

        assert metatag_leaf.tag == self.tag
        assert metatag_leaf.title == self.title
        assert metatag_leaf.leaves == []

    def test_de_json_all(self, client, metatag_leaf_nested):
        json_dict = {
            'tag': self.tag,
            'title': self.title,
            'leaves': [metatag_leaf_nested.to_dict()],
        }
        metatag_leaf = MetatagLeaf.de_json(json_dict, client)

        assert metatag_leaf.tag == self.tag
        assert metatag_leaf.title == self.title
        assert metatag_leaf.leaves == [metatag_leaf_nested]

    def test_equality(self, metatag_leaf_nested):
        a = MetatagLeaf(tag=self.tag, title=self.title, leaves=[metatag_leaf_nested])
        b = MetatagLeaf(tag='other', title=self.title, leaves=[metatag_leaf_nested])
        c = MetatagLeaf(tag=self.tag, title=self.title, leaves=[metatag_leaf_nested])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
