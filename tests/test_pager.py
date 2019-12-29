from yandex_music import Pager


class TestPager:
    total = 4
    page = 0
    per_page = 4

    def test_expected_values(self, pager):
        assert pager.total == self.total
        assert pager.page == self.page
        assert pager.per_page == self.per_page

    def test_de_json_none(self, client):
        assert Pager.de_json({}, client) is None

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
        a = Pager(self.total, self.page, self.per_page)
        b = Pager(0, self.page, self.per_page)
        c = Pager(self.total, 0, 0)
        d = Pager(self.total, self.page, self.per_page)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
