from yandex_music import LyricsMajor


class TestLyricsMajor:
    id = 560
    name = 'MUSIXMATCH'
    pretty_name = 'Musixmatch'

    def test_expected_values(self, lyrics_major):
        assert lyrics_major.id == self.id
        assert lyrics_major.name == self.name
        assert lyrics_major.pretty_name == self.pretty_name

    def test_de_json_none(self, client):
        assert LyricsMajor.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'id': self.id, 'name': self.name, 'pretty_name': self.pretty_name}

        lyrics_major = LyricsMajor.de_json(json_dict, client)
        assert lyrics_major.id == self.id
        assert lyrics_major.name == self.name
        assert lyrics_major.pretty_name == self.pretty_name

    def test_de_json_all(self, client):
        json_dict = {'id': self.id, 'name': self.name, 'pretty_name': self.pretty_name}

        lyrics_major = LyricsMajor.de_json(json_dict, client)
        assert lyrics_major.id == self.id
        assert lyrics_major.name == self.name
        assert lyrics_major.pretty_name == self.pretty_name

    def test_equality(self):
        a = LyricsMajor(self.id, self.name, self.pretty_name)
        b = LyricsMajor(10, self.name, self.pretty_name)
        c = LyricsMajor(self.id, self.name, self.pretty_name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
