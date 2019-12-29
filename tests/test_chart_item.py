from yandex_music import ChartItem


class TestChartItem:
    def test_expected_values(self, chart_item, track, chart):
        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_de_json_none(self, client):
        assert ChartItem.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert ChartItem.de_list({}, client) == []

    def test_de_json_required(self, client, track, chart):
        json_dict = {'track': track.to_dict(), 'chart': chart.to_dict()}
        chart_item = ChartItem.de_json(json_dict, client)

        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_de_json_all(self, client, track, chart):
        json_dict = {'track': track.to_dict(), 'chart': chart.to_dict()}
        chart_item = ChartItem.de_json(json_dict, client)

        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_equality(self, track, chart):
        a = ChartItem(track, chart)
        b = ChartItem(None, chart)
        c = ChartItem(track, chart)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
