import pytest

from yandex_music import ChartItem


@pytest.fixture(scope='class')
def chart_item(track, chart):
    return ChartItem(track, chart)


class TestChartItem:

    def test_expected_values(self, chart_item, track, chart):
        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_de_json_required(self, client, track, chart):
        json_dict = {'track': track, 'chart': chart}
        chart_item = ChartItem.de_json(json_dict, client)

        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_de_json_all(self, client, track, chart):
        json_dict = {'track': track, 'chart': chart}
        chart_item = ChartItem.de_json(json_dict, client)

        assert chart_item.track == track
        assert chart_item.chart == chart

    def test_equality(self):
        pass
