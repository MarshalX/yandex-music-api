from yandex_music import TrackPosition


class TestTrackPosition:
    volume = None
    index = None

    def test_expected_values(self, track_position):
        assert track_position.volume == self.volume
        assert track_position.index == self.index

    def test_de_json_required(self, client):
        json_dict = {'volume': self.volume, 'index': self.index}
        track_position = TrackPosition.de_json(json_dict, client)

        assert track_position.volume == self.volume
        assert track_position.index == self.index

    def test_de_json_all(self, client):
        json_dict = {'volume': self.volume, 'index': self.index}
        track_position = TrackPosition.de_json(json_dict, client)

        assert track_position.volume == self.volume
        assert track_position.index == self.index

    def test_equality(self):
        pass
