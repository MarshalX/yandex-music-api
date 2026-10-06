from typing import Dict, Tuple

import pytest

from tests import TestBest
from yandex_music import Album, Artist, Best, Client, JSONType, Playlist, Suggestions, Track, Video, YandexMusicModel


@pytest.fixture(scope='class', params=[1, 2, 3, 4, 5])
def suggestions_with_best(
    request: pytest.FixtureRequest, results: Dict[int, YandexMusicModel], types: Dict[int, str]
) -> Tuple[Suggestions, Best]:
    param: int = request.param
    result = results[param]
    assert isinstance(result, (Track, Artist, Album, Playlist, Video))
    best = Best(types[param], result, TestBest.text)
    return Suggestions(best, TestSuggestions.suggestions), best


class TestSuggestions:
    suggestions = [
        'empathy test',
        'testament',
        'crash test dummies',
        'seekae - test & recognise',
        'joji - test drive',
        'john powell - test drive',
        'max richter - testament of youth',
        'seekae - test & recognise',
        'testament - first strike still deadly',
        '90-е в стиле r&b и соул',
        'crash test dummy: из чего состоит portishead',
        'в стиле: alice testrup',
    ]

    def test_expected_values(self, suggestions_with_best: Tuple[Suggestions, Best]) -> None:
        suggestions, best = suggestions_with_best

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_de_json_none(self, client: Client) -> None:
        assert Suggestions.de_json({}, client) is None

    def test_de_json_required(self, client: Client, best: Best) -> None:
        json_dict: Dict[str, JSONType] = {'best': best.to_dict(), 'suggestions': self.suggestions}
        suggestions = Suggestions.de_json(json_dict, client)
        assert suggestions is not None

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_de_json_all(self, client: Client, best: Best) -> None:
        json_dict: Dict[str, JSONType] = {'best': best.to_dict(), 'suggestions': self.suggestions}
        suggestions = Suggestions.de_json(json_dict, client)
        assert suggestions is not None

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_equality(self, best: Best) -> None:
        a = Suggestions(best, self.suggestions)
        b = Suggestions(None, self.suggestions)
        c = Suggestions(best, [])
        d = Suggestions(best, self.suggestions)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
