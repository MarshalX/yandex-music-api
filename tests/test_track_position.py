from typing import Dict

from yandex_music import Client, JSONType, TrackPosition


class TestTrackPosition:
    volume = 1
    index = 10

    def test_expected_values(self, track_position: TrackPosition) -> None:
        assert track_position.volume == self.volume
        assert track_position.index == self.index

    def test_de_json_none(self, client: Client) -> None:
        assert TrackPosition.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'volume': self.volume, 'index': self.index}
        track_position = TrackPosition.de_json(json_dict, client)
        assert track_position is not None

        assert track_position.volume == self.volume
        assert track_position.index == self.index

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'volume': self.volume, 'index': self.index}
        track_position = TrackPosition.de_json(json_dict, client)
        assert track_position is not None

        assert track_position.volume == self.volume
        assert track_position.index == self.index

    def test_equality(self) -> None:
        a = TrackPosition(self.volume, self.index)
        b = TrackPosition(5, self.index)
        c = TrackPosition(self.volume, 10)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
