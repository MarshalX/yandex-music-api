import pytest

from yandex_music import SearchResult


@pytest.fixture(scope='class')
def search_result():
    return SearchResult(TestSearchResult.total, TestSearchResult.per_page, TestSearchResult.order,
                        TestSearchResult.results)


class TestSearchResult:
    total = None
    per_page = None
    order = None

    def test_expected_values(self, search_result, results):
        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == results

    def test_de_json_required(self, client, results):
        json_dict = {'total': self.total, 'per_page': self.per_page, 'order': self.order, 'results': results}
        search_result = SearchResult.de_json(json_dict, client)

        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == results

    def test_de_json_all(self, client, results):
        json_dict = {'total': self.total, 'per_page': self.per_page, 'order': self.order, 'results': results}
        search_result = SearchResult.de_json(json_dict, client)

        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == results

    def test_equality(self):
        pass
