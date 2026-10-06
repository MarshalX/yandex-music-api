from typing import Dict

from yandex_music import Chart, ChartItem, Client, JSONType, Track


class TestChartItem:
    def test_expected_values(self, chart_item: ChartItem, track: Track, chart: Chart) -> None:
        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_de_json_none(self, client: Client) -> None:
        assert ChartItem.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert ChartItem.de_list([], client) == []

    def test_de_json_required(self, client: Client, track: Track, chart: Chart) -> None:
        json_dict: Dict[str, JSONType] = {'track': track.to_dict(), 'chart': chart.to_dict()}
        chart_item = ChartItem.de_json(json_dict, client)
        assert chart_item is not None

        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_de_json_all(self, client: Client, track: Track, chart: Chart) -> None:
        json_dict: Dict[str, JSONType] = {'track': track.to_dict(), 'chart': chart.to_dict()}
        chart_item = ChartItem.de_json(json_dict, client)
        assert chart_item is not None

        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_equality(self, track: Track, chart: Chart) -> None:
        a = ChartItem(track, chart)
        b = ChartItem(None, chart)
        c = ChartItem(track, chart)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
