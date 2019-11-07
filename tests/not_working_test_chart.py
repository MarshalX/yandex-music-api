from yandex_music import Chart


class TestChart:
    position = None
    progress = None
    listeners = None
    shift = None

    def test_expected_values(self, chart, track_id):
        assert chart.position == self.position
        assert chart.progress == self.progress
        assert chart.listeners == self.listeners
        assert chart.shift == self.shift
        assert chart.track_id == track_id

    def test_de_json_required(self, client):
        json_dict = {'position': self.position, 'progress': self.progress, 'listeners': self.listeners,
                     'shift': self.shift}
        chart = Chart.de_json(json_dict, client)

        assert chart.position == self.position
        assert chart.progress == self.progress
        assert chart.listeners == self.listeners
        assert chart.shift == self.shift

    def test_de_json_all(self, client, track_id):
        json_dict = {'position': self.position, 'progress': self.progress, 'listeners': self.listeners,
                     'shift': self.shift, 'track_id': track_id}
        chart = Chart.de_json(json_dict, client)

        assert chart.position == self.position
        assert chart.progress == self.progress
        assert chart.listeners == self.listeners
        assert chart.shift == self.shift
        assert chart.track_id == track_id

    def test_equality(self):
        pass
