from yandex_music import SearchResult


class TestSearchResult:
    total = 3
    per_page = 10
    order = 0

    def test_expected_values(self, search_result_with_results):
        search_result, results = search_result_with_results

        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == results

    def test_de_json_required(self, client, result_with_type):
        result, type = result_with_type

        json_dict = {'total': self.total, 'per_page': self.per_page, 'order': self.order, 'results': [result.to_dict()]}
        search_result = SearchResult.de_json(json_dict, client, type)

        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == [result]

    def test_de_json_all(self, client, result_with_type):
        result, type = result_with_type

        json_dict = {'total': self.total, 'per_page': self.per_page, 'order': self.order, 'results': [result.to_dict()]}
        search_result = SearchResult.de_json(json_dict, client, type)

        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == [result]

    def test_equality(self, result_with_type):
        result, _ = result_with_type

        a = SearchResult(self.total, self.per_page, self.order, [result])
        b = SearchResult(10, self.per_page, 1, [result])
        c = SearchResult(self.total, self.per_page, self.order, [result])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
