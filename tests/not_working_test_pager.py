from yandex_music import Pager


class TestPager:
    total = None
    page = None
    per_page = None

    def test_expected_values(self, pager):
        assert pager.total == self.total
        assert pager.page == self.page
        assert pager.per_page == self.per_page

    def test_de_json_required(self, client):
        json_dict = {'total': self.total, 'page': self.page, 'per_page': self.per_page}
        pager = Pager.de_json(json_dict, client)

        assert pager.total == self.total
        assert pager.page == self.page
        assert pager.per_page == self.per_page

    def test_de_json_all(self, client):
        json_dict = {'total': self.total, 'page': self.page, 'per_page': self.per_page}
        pager = Pager.de_json(json_dict, client)

        assert pager.total == self.total
        assert pager.page == self.page
        assert pager.per_page == self.per_page

    def test_equality(self):
        pass
