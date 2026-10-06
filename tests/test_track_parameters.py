from typing import Dict

from yandex_music import Client, Fade, JSONType, TrackParameters


class TestTrackParameters:
    bpm = 120
    energy = 0.5
    hue = 23.0
    user_collection_hue = 23

    def test_expected_values(self, track_parameters: TrackParameters, fade: Fade) -> None:
        assert track_parameters.bpm == self.bpm
        assert track_parameters.energy == self.energy
        assert track_parameters.hue == self.hue
        assert track_parameters.user_collection_hue == self.user_collection_hue
        assert track_parameters.mix_fade == fade

    def test_de_json_none(self, client: Client) -> None:
        assert TrackParameters.de_json({}, client) is None

    def test_de_json_all(self, client: Client, fade: Fade) -> None:
        json_dict: Dict[str, JSONType] = {
            'bpm': self.bpm,
            'energy': self.energy,
            'hue': self.hue,
            'userCollectionHue': self.user_collection_hue,
            'mixFade': fade.to_dict(),
        }
        track_parameters = TrackParameters.de_json(json_dict, client)
        assert track_parameters is not None

        assert track_parameters.bpm == self.bpm
        assert track_parameters.energy == self.energy
        assert track_parameters.hue == self.hue
        assert track_parameters.user_collection_hue == self.user_collection_hue
        assert track_parameters.mix_fade == fade

    def test_equality(self) -> None:
        a = TrackParameters(self.bpm, self.energy, self.hue)
        b = TrackParameters(90, self.energy, self.hue)
        c = TrackParameters(self.bpm, self.energy, self.hue)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
