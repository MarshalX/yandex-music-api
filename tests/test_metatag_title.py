from yandex_music import MetatagTitle


class TestMetatagTitle:
    title = 'Рок'
    full_title = 'Рок-музыка'

    def test_expected_values(self, metatag_title):
        assert metatag_title.title == self.title
        assert metatag_title.full_title == self.full_title

    def test_de_json_none(self, client):
        assert MetatagTitle.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'title': self.title, 'fullTitle': self.full_title}
        metatag_title = MetatagTitle.de_json(json_dict, client)

        assert metatag_title.title == self.title
        assert metatag_title.full_title == self.full_title

    def test_equality(self):
        a = MetatagTitle(title=self.title, full_title=self.full_title)
        b = MetatagTitle(title='other', full_title=self.full_title)
        c = MetatagTitle(title=self.title, full_title=self.full_title)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
