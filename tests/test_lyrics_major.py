from typing import Dict

from yandex_music import Client, JSONType, LyricsMajor


class TestLyricsMajor:
    id = 560
    name = 'MUSIXMATCH'
    pretty_name = 'Musixmatch'

    def test_expected_values(self, lyrics_major: LyricsMajor) -> None:
        assert lyrics_major.id == self.id
        assert lyrics_major.name == self.name
        assert lyrics_major.pretty_name == self.pretty_name

    def test_de_json_none(self, client: Client) -> None:
        assert LyricsMajor.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id, 'name': self.name, 'pretty_name': self.pretty_name}

        lyrics_major = LyricsMajor.de_json(json_dict, client)
        assert lyrics_major is not None
        assert lyrics_major.id == self.id
        assert lyrics_major.name == self.name
        assert lyrics_major.pretty_name == self.pretty_name

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id, 'name': self.name, 'pretty_name': self.pretty_name}

        lyrics_major = LyricsMajor.de_json(json_dict, client)
        assert lyrics_major is not None
        assert lyrics_major.id == self.id
        assert lyrics_major.name == self.name
        assert lyrics_major.pretty_name == self.pretty_name

    def test_equality(self) -> None:
        a = LyricsMajor(self.id, self.name, self.pretty_name)
        b = LyricsMajor(10, self.name, self.pretty_name)
        c = LyricsMajor(self.id, self.name, self.pretty_name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
