import pytest

from tests import TestBest

from yandex_music import Suggestions, Best


@pytest.fixture(scope='class', params=[1, 2, 3, 4, 5])
def suggestions_with_best(request, results, types):
    best = Best(types[request.param], results[request.param], TestBest.text)
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

    def test_expected_values(self, suggestions_with_best):
        suggestions, best = suggestions_with_best

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_de_json_none(self, client):
        assert Suggestions.de_json({}, client) is None

    def test_de_json_required(self, client, best):
        json_dict = {'best': best.to_dict(), 'suggestions': self.suggestions}
        suggestions = Suggestions.de_json(json_dict, client)

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_de_json_all(self, client, best):
        json_dict = {'best': best.to_dict(), 'suggestions': self.suggestions}
        suggestions = Suggestions.de_json(json_dict, client)

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_equality(self, best):
        a = Suggestions(best, self.suggestions)
        b = Suggestions(None, self.suggestions)
        c = Suggestions(best, [])
        d = Suggestions(best, self.suggestions)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
