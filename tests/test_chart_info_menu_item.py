from typing import Dict

from yandex_music import ChartInfoMenuItem, Client, JSONType


class TestChartInfoMenuItem:
    title = 'Россия'
    url = 'russia'
    selected = True

    def test_expected_values(self, chart_info_menu_item: ChartInfoMenuItem) -> None:
        assert chart_info_menu_item.title == self.title
        assert chart_info_menu_item.url == self.url
        assert chart_info_menu_item.selected == self.selected

    def test_de_json_none(self, client: Client) -> None:
        assert ChartInfoMenuItem.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'url': self.url,
        }

        chart_info_menu_item = ChartInfoMenuItem.de_json(json_dict, client)

        assert chart_info_menu_item is not None

        assert chart_info_menu_item.title == self.title
        assert chart_info_menu_item.url == self.url

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'url': self.url,
            'selected': self.selected,
        }

        chart_info_menu_item = ChartInfoMenuItem.de_json(json_dict, client)

        assert chart_info_menu_item is not None

        assert chart_info_menu_item.title == self.title
        assert chart_info_menu_item.url == self.url
        assert chart_info_menu_item.selected == self.selected

    def test_equality(self) -> None:
        a = ChartInfoMenuItem(self.title, self.url, self.selected)
        b = ChartInfoMenuItem(self.title, 'no_url', self.selected)
        c = ChartInfoMenuItem(self.title, self.url, self.selected)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
