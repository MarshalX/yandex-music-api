from yandex_music import Chart


class TestChart:
    position = 2
    progress = 'same'
    listeners = 1433
    shift = 0
    bg_color = '#666A61'

    def test_expected_values(self, chart, track_id):
        assert chart.position == self.position
        assert chart.progress == self.progress
        assert chart.listeners == self.listeners
        assert chart.shift == self.shift
        assert chart.track_id == track_id
        assert chart.bg_color == self.bg_color

    def test_de_json_none(self, client):
        assert Chart.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Chart.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {
            'position': self.position,
            'progress': self.progress,
            'listeners': self.listeners,
            'shift': self.shift,
        }
        chart = Chart.de_json(json_dict, client)

        assert chart.position == self.position
        assert chart.progress == self.progress
        assert chart.listeners == self.listeners
        assert chart.shift == self.shift

    def test_de_json_all(self, client, track_id):
        json_dict = {
            'position': self.position,
            'progress': self.progress,
            'listeners': self.listeners,
            'shift': self.shift,
            'bg_color': self.bg_color,
            'track_id': track_id.to_dict(),
        }
        chart = Chart.de_json(json_dict, client)

        assert chart.position == self.position
        assert chart.progress == self.progress
        assert chart.listeners == self.listeners
        assert chart.shift == self.shift
        assert chart.track_id == track_id
        assert chart.bg_color == self.bg_color

    def test_equality(self):
        a = Chart(self.position, self.progress, self.listeners, self.shift)
        b = Chart(10, self.progress, self.listeners, self.shift)
        c = Chart(self.position, self.progress, 10, self.shift)
        d = Chart(self.position, self.progress, self.listeners, self.shift)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
