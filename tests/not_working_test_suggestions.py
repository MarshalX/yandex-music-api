import pytest

from yandex_music import Suggestions


@pytest.fixture(scope='class')
def suggestions(best):
    return Suggestions(best, TestSuggestions.suggestions)


class TestSuggestions:
    suggestions = None

    def test_expected_values(self, suggestions, best):
        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_de_json_required(self, client, best):
        json_dict = {'best': best, 'suggestions': self.suggestions}
        suggestions = Suggestions.de_json(json_dict, client)

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_de_json_all(self, client, best):
        json_dict = {'best': best, 'suggestions': self.suggestions}
        suggestions = Suggestions.de_json(json_dict, client)

        assert suggestions.best == best
        assert suggestions.suggestions == self.suggestions

    def test_equality(self):
        pass
