from typing import Dict

from yandex_music import Client, JSONType, Sequence, Track, TrackParameters


class TestSequence:
    type = 'track'
    liked = False

    def test_expected_values(self, sequence: Sequence, track: Track, track_parameters: TrackParameters) -> None:
        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked
        assert sequence.track_parameters == track_parameters

    def test_de_json_none(self, client: Client) -> None:
        assert Sequence.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Sequence.de_list([], client) == []

    def test_de_json_required(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type, 'track': track.to_dict(), 'liked': self.liked}
        sequence = Sequence.de_json(json_dict, client)
        assert sequence is not None

        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_de_json_all(self, client: Client, track: Track, track_parameters: TrackParameters) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'track': track.to_dict(),
            'liked': self.liked,
            'trackParameters': track_parameters.to_dict(),
        }
        sequence = Sequence.de_json(json_dict, client)
        assert sequence is not None

        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked
        assert sequence.track_parameters == track_parameters

    def test_equality(self, track: Track) -> None:
        a = Sequence(self.type, track, self.liked)
        b = Sequence('', track, True)
        c = Sequence(self.type, track, self.liked)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
