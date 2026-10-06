from typing import Dict

from yandex_music import Client, JSONType, PoetryLoverMatch


class TestPoetryLoverMatch:
    begin = 18
    end = 25
    line = 3

    def test_expected_values(self, poetry_lover_match: PoetryLoverMatch) -> None:
        assert poetry_lover_match.begin == self.begin
        assert poetry_lover_match.end == self.end
        assert poetry_lover_match.line == self.line

    def test_de_json_none(self, client: Client) -> None:
        assert PoetryLoverMatch.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert PoetryLoverMatch.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'begin': self.begin, 'end': self.end, 'line': self.line}
        poetry_lover_match = PoetryLoverMatch.de_json(json_dict, client)
        assert poetry_lover_match is not None

        assert poetry_lover_match.begin == self.begin
        assert poetry_lover_match.end == self.end
        assert poetry_lover_match.line == self.line

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'begin': self.begin, 'end': self.end, 'line': self.line}
        poetry_lover_match = PoetryLoverMatch.de_json(json_dict, client)
        assert poetry_lover_match is not None

        assert poetry_lover_match.begin == self.begin
        assert poetry_lover_match.end == self.end
        assert poetry_lover_match.line == self.line

    def test_equality(self) -> None:
        a = PoetryLoverMatch(self.begin, self.end, self.line)
        b = PoetryLoverMatch(self.begin, 10, self.line)
        c = PoetryLoverMatch(self.begin, self.end, self.line)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
