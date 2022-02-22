from yandex_music import Sequence


class TestSequence:
    type = 'track'
    liked = False

    def test_expected_values(self, sequence, track):
        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_de_json_none(self, client):
        assert Sequence.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Sequence.de_list({}, client) == []

    def test_de_json_required(self, client, track):
        json_dict = {'type': self.type, 'track': track.to_dict(), 'liked': self.liked}
        sequence = Sequence.de_json(json_dict, client)

        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_de_json_all(self, client, track):
        json_dict = {'type': self.type, 'track': track.to_dict(), 'liked': self.liked}
        sequence = Sequence.de_json(json_dict, client)

        assert sequence.type == self.type
        assert sequence.track == track
        assert sequence.liked == self.liked

    def test_equality(self, track):
        a = Sequence(self.type, track, self.liked)
        b = Sequence('', track, True)
        c = Sequence(self.type, track, self.liked)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
