from yandex_music import Metatags


class TestMetatags:
    def test_expected_values(self, metatags, metatag_tree):
        assert metatags.trees == [metatag_tree]

    def test_de_json_none(self, client):
        assert Metatags.de_json({}, client) is None

    def test_de_json_all(self, client, metatag_tree):
        json_dict = {'trees': [metatag_tree.to_dict()]}
        metatags = Metatags.de_json(json_dict, client)

        assert metatags.trees == [metatag_tree]

    def test_equality(self, metatag_tree):
        a = Metatags(trees=[metatag_tree])
        b = Metatags(trees=[])
        c = Metatags(trees=[metatag_tree])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, metatags):
        assert len(metatags) == len(metatags.trees)

    def test_getitem(self, metatags):
        assert metatags[0] == metatags.trees[0]

    def test_iter(self, metatags):
        assert list(metatags) == metatags.trees
