from yandex_music import TrackParameters


class TestTrackParameters:
    bpm = 120
    energy = 0.5
    hue = 23.0
    user_collection_hue = 23

    def test_expected_values(self, track_parameters, fade):
        assert track_parameters.bpm == self.bpm
        assert track_parameters.energy == self.energy
        assert track_parameters.hue == self.hue
        assert track_parameters.user_collection_hue == self.user_collection_hue
        assert track_parameters.mix_fade == fade

    def test_de_json_none(self, client):
        assert TrackParameters.de_json({}, client) is None

    def test_de_json_all(self, client, fade):
        json_dict = {
            'bpm': self.bpm,
            'energy': self.energy,
            'hue': self.hue,
            'userCollectionHue': self.user_collection_hue,
            'mixFade': fade.to_dict(),
        }
        track_parameters = TrackParameters.de_json(json_dict, client)

        assert track_parameters.bpm == self.bpm
        assert track_parameters.energy == self.energy
        assert track_parameters.hue == self.hue
        assert track_parameters.user_collection_hue == self.user_collection_hue
        assert track_parameters.mix_fade == fade

    def test_equality(self):
        a = TrackParameters(self.bpm, self.energy, self.hue)
        b = TrackParameters(90, self.energy, self.hue)
        c = TrackParameters(self.bpm, self.energy, self.hue)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
