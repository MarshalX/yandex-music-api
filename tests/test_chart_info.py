from yandex_music import ChartInfo


class TestChartInfo:
    id = 'KpXst7X4'
    type = 'chart'
    type_for_from = 'chart'
    title = 'Треки, популярные на Яндекс.Музыке прямо сейчас'
    chart_description = 'Слушателей за день'

    def test_expected_values(self, chart_info, chart_info_menu, playlist):
        assert chart_info.id == self.id
        assert chart_info.type == self.type
        assert chart_info.type_for_from == self.type_for_from
        assert chart_info.title == self.title
        assert chart_info.chart == playlist
        assert chart_info.menu == chart_info_menu

    def test_de_json_none(self, client):
        assert ChartInfo.de_json({}, client) is None

    def test_de_json_required(self, playlist, chart_info_menu, client):
        json_dict = {
            'id': self.id,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'chart_description': self.chart_description,
            'menu': chart_info_menu.to_dict(),
            'chart': playlist.to_dict(),
        }

        chart_info = ChartInfo.de_json(json_dict, client)

        assert chart_info.id == self.id
        assert chart_info.type == self.type
        assert chart_info.type_for_from == self.type_for_from
        assert chart_info.title == self.title
        assert chart_info.chart_description == self.chart_description

    def test_de_json_all(self, client, playlist, chart_info_menu):
        json_dict = {
            'id': self.id,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'chart_description': self.chart_description,
            'menu': chart_info_menu.to_dict(),
            'chart': playlist.to_dict(),
        }

        chart_info = ChartInfo.de_json(json_dict, client)

        assert chart_info.id == self.id
        assert chart_info.type == self.type
        assert chart_info.type_for_from == self.type_for_from
        assert chart_info.title == self.title
        assert chart_info.chart_description == self.chart_description
        assert chart_info.menu == chart_info_menu
        assert chart_info.chart == playlist

    def test_equality(self, playlist, chart_info_menu):
        a = ChartInfo(
            self.id, self.type, self.type_for_from, self.title, self.chart_description, chart_info_menu, playlist
        )
        b = ChartInfo(
            "no_id", self.type, self.type_for_from, self.title, self.chart_description, chart_info_menu, playlist
        )
        c = ChartInfo(
            self.id, self.type, self.type_for_from, self.title, self.chart_description, chart_info_menu, playlist
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
