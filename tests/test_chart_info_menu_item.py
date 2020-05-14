from yandex_music import ChartInfoMenuItem


class TestChartInfoMenuItem:
    title = 'Россия'
    url = 'russia'
    selected = True

    def test_expected_values(self, chart_info_menu_item):
        assert chart_info_menu_item.title == self.title
        assert chart_info_menu_item.url == self.url
        assert chart_info_menu_item.selected == self.selected

    def test_de_json_none(self, client):
        assert ChartInfoMenuItem.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'title': self.title,
            'url': self.url,
        }

        chart_info_menu_item = ChartInfoMenuItem.de_json(json_dict, client)

        assert chart_info_menu_item.title == self.title
        assert chart_info_menu_item.url == self.url

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'url': self.url,
            'selected': self.selected,
        }

        chart_info_menu_item = ChartInfoMenuItem.de_json(json_dict, client)

        assert chart_info_menu_item.title == self.title
        assert chart_info_menu_item.url == self.url
        assert chart_info_menu_item.selected == self.selected

    def test_equality(self):
        a = ChartInfoMenuItem(self.title, self.url, self.selected)
        b = ChartInfoMenuItem(self.title, "no_url", self.selected)
        c = ChartInfoMenuItem(self.title, self.url, self.selected)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
