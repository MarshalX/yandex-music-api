from yandex_music import ChartInfo


class TestChartInfo:
    id = 'KpXst7X4'
    type = 'chart'
    menu = {
        'items': [
            {'title': 'Россия', 'url': 'russia', 'selected': True},
            {'title': 'Глобальный чарт', 'url': 'world'}
        ]
    }
    type_for_from = 'chart'
    title = 'Треки, популярные на Яндекс.Музыке прямо сейчас'
    chart_description = 'Слушателей за день'

    def test_expected_values(self, chartInfo, playlist):
        assert chartInfo.id == self.id
        assert chartInfo.type == self.type
        assert chartInfo.type_for_from == self.type_for_from
        assert chartInfo.title == self.title
        assert chartInfo.chart == playlist

    def test_de_json_none(self, client):
        assert ChartInfo.de_json({}, client) is None

    def test_de_json_required(self, playlist, client):
        json_dict = {
            'id_': self.id,
            'type_': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'chart_description': self.chart_description,
            'menu': self.menu,
            'chart': playlist.to_dict()
        }

        chartInfo = ChartInfo.de_json(json_dict, client)

        assert chartInfo.id == self.id
        assert chartInfo.type == self.type
        assert chartInfo.type_for_from == self.type_for_from
        assert chartInfo.title == self.title
        assert chartInfo.chart_description == self.chart_description

    def test_de_json_all(self, client, playlist):
        json_dict = {
            'id_': self.id,
            'type_': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'chart_description': self.chart_description,
            'menu': self.menu,
            'chart': playlist.to_dict()
        }

        chartInfo = ChartInfo.de_json(json_dict, client)

        assert chartInfo.id == self.id
        assert chartInfo.type == self.type
        assert chartInfo.type_for_from == self.type_for_from
        assert chartInfo.title == self.title
        assert chartInfo.chart_description == self.chart_description
        assert chartInfo.menu == self.menu
        assert chartInfo.chart == playlist
