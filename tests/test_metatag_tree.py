from yandex_music import MetatagTree


class TestMetatagTree:
    title = 'Настроения'
    navigation_id = 'moods'

    def test_expected_values(self, metatag_tree, metatag_leaf):
        assert metatag_tree.title == self.title
        assert metatag_tree.navigation_id == self.navigation_id
        assert metatag_tree.leaves == [metatag_leaf]

    def test_de_json_none(self, client):
        assert MetatagTree.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'title': self.title, 'navigationId': self.navigation_id}
        metatag_tree = MetatagTree.de_json(json_dict, client)

        assert metatag_tree.title == self.title
        assert metatag_tree.navigation_id == self.navigation_id
        assert metatag_tree.leaves == []

    def test_de_json_all(self, client, metatag_leaf):
        json_dict = {
            'title': self.title,
            'navigationId': self.navigation_id,
            'leaves': [metatag_leaf.to_dict()],
        }
        metatag_tree = MetatagTree.de_json(json_dict, client)

        assert metatag_tree.title == self.title
        assert metatag_tree.navigation_id == self.navigation_id
        assert metatag_tree.leaves == [metatag_leaf]

    def test_equality(self, metatag_leaf):
        a = MetatagTree(title=self.title, navigation_id=self.navigation_id, leaves=[metatag_leaf])
        b = MetatagTree(title=self.title, navigation_id='other', leaves=[metatag_leaf])
        c = MetatagTree(title=self.title, navigation_id=self.navigation_id, leaves=[metatag_leaf])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
