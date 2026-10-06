from typing import Dict

from yandex_music import ChartInfo, ChartInfoMenu, Client, JSONType, Playlist


class TestChartInfo:
    id = 'KpXst7X4'
    type = 'chart'
    type_for_from = 'chart'
    title = 'Треки, популярные на Яндекс.Музыке прямо сейчас'
    chart_description = 'Слушателей за день'

    def test_expected_values(self, chart_info: ChartInfo, chart_info_menu: ChartInfoMenu, playlist: Playlist) -> None:
        assert chart_info.id == self.id
        assert chart_info.type == self.type
        assert chart_info.type_for_from == self.type_for_from
        assert chart_info.title == self.title
        assert chart_info.chart == playlist
        assert chart_info.menu == chart_info_menu

    def test_de_json_none(self, client: Client) -> None:
        assert ChartInfo.de_json({}, client) is None

    def test_de_json_required(self, playlist: Playlist, chart_info_menu: ChartInfoMenu, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'chart_description': self.chart_description,
            'menu': chart_info_menu.to_dict(),
            'chart': playlist.to_dict(),
        }

        chart_info = ChartInfo.de_json(json_dict, client)

        assert chart_info is not None

        assert chart_info.id == self.id
        assert chart_info.type == self.type
        assert chart_info.type_for_from == self.type_for_from
        assert chart_info.title == self.title
        assert chart_info.chart_description == self.chart_description

    def test_de_json_all(self, client: Client, playlist: Playlist, chart_info_menu: ChartInfoMenu) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'chart_description': self.chart_description,
            'menu': chart_info_menu.to_dict(),
            'chart': playlist.to_dict(),
        }

        chart_info = ChartInfo.de_json(json_dict, client)

        assert chart_info is not None

        assert chart_info.id == self.id
        assert chart_info.type == self.type
        assert chart_info.type_for_from == self.type_for_from
        assert chart_info.title == self.title
        assert chart_info.chart_description == self.chart_description
        assert chart_info.menu == chart_info_menu
        assert chart_info.chart == playlist

    def test_equality(self, playlist: Playlist, chart_info_menu: ChartInfoMenu) -> None:
        a = ChartInfo(
            self.id, self.type, self.type_for_from, self.title, chart_info_menu, playlist, self.chart_description
        )
        b = ChartInfo(
            'no_id', self.type, self.type_for_from, self.title, chart_info_menu, playlist, self.chart_description
        )
        c = ChartInfo(
            self.id, self.type, self.type_for_from, self.title, chart_info_menu, playlist, self.chart_description
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
