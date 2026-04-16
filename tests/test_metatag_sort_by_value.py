from yandex_music import MetatagSortByValue


class TestMetatagSortByValue:
    value = 'popular'
    title = 'Сначала популярные'
    active = True

    def test_expected_values(self, metatag_sort_by_value):
        assert metatag_sort_by_value.value == self.value
        assert metatag_sort_by_value.title == self.title
        assert metatag_sort_by_value.active == self.active

    def test_de_json_none(self, client):
        assert MetatagSortByValue.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'value': self.value, 'title': self.title, 'active': self.active}
        metatag_sort_by_value = MetatagSortByValue.de_json(json_dict, client)

        assert metatag_sort_by_value.value == self.value
        assert metatag_sort_by_value.title == self.title
        assert metatag_sort_by_value.active == self.active

    def test_equality(self):
        a = MetatagSortByValue(value=self.value, title=self.title, active=self.active)
        b = MetatagSortByValue(value='new', title=self.title, active=self.active)
        c = MetatagSortByValue(value=self.value, title=self.title, active=self.active)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
