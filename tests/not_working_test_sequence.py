from yandex_music import Sequence


class TestSequence:
    type = None
    liked = None

    def test_expected_values(self, sequence, track):
        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_de_json_required(self, client, track):
        json_dict = {'type': self.type, 'track': track, 'liked': self.liked}
        sequence = Sequence.de_json(json_dict, client)

        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_de_json_all(self, client, track):
        json_dict = {'type': self.type, 'track': track, 'liked': self.liked}
        sequence = Sequence.de_json(json_dict, client)

        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_equality(self):
        pass
