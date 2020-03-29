from yandex_music import ChartInfoMenu, ChartInfoMenuItem


class TestChartInfoMenu:
    def test_expected_values(self, chart_info_menu, chart_info_menu_item):
        assert chart_info_menu.items == [chart_info_menu_item]

    def test_de_json_none(self, client):
        assert ChartInfoMenu.de_json({}, client) is None

    def test_de_json_required(self, chart_info_menu_item, client):
        json_dict = {
            'items': [chart_info_menu_item.to_dict()],
        }

        chart_info_menu = ChartInfoMenu.de_json(json_dict, client)

        assert chart_info_menu.items == [chart_info_menu_item]

    def test_equality(self, chart_info_menu_item):
        a = ChartInfoMenu([chart_info_menu_item])
        b = ChartInfoMenu([ChartInfoMenuItem("tt", "no_url")])
        c = ChartInfoMenu([chart_info_menu_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
