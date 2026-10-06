from typing import Dict, List, Tuple, Union

from yandex_music import Album, Artist, Client, JSONType, Playlist, SearchResult, Track, User, Video

SearchItem = Union[Track, Artist, Album, Playlist, Video, User]


class TestSearchResult:
    total = 3
    per_page = 10
    order = 0

    def test_expected_values(
        self, search_result_with_results_and_type: Tuple[SearchResult[SearchItem], List[SearchItem], str]
    ) -> None:
        search_result, results, type_ = search_result_with_results_and_type

        assert search_result.type == type_
        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == results

    def test_de_json_none(self, client: Client) -> None:
        assert SearchResult.de_json({}, client) is None

    def test_de_json_required(self, client: Client, result_with_type: Tuple[SearchItem, str]) -> None:
        result, type_ = result_with_type

        json_dict: Dict[str, JSONType] = {
            'total': self.total,
            'per_page': self.per_page,
            'order': self.order,
            'results': [result.to_dict()],
        }
        search_result = SearchResult.de_json(json_dict, client, type_)
        assert search_result is not None

        assert search_result.type == type_
        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == [result]

    def test_de_json_all(self, client: Client, result_with_type: Tuple[SearchItem, str]) -> None:
        result, type_ = result_with_type

        json_dict: Dict[str, JSONType] = {
            'total': self.total,
            'per_page': self.per_page,
            'order': self.order,
            'results': [result.to_dict()],
        }
        search_result = SearchResult.de_json(json_dict, client, type_)
        assert search_result is not None

        assert search_result.type == type_
        assert search_result.total == self.total
        assert search_result.per_page == self.per_page
        assert search_result.order == self.order
        assert search_result.results == [result]

    def test_equality(self, result_with_type: Tuple[SearchItem, str]) -> None:
        result, type_ = result_with_type

        a = SearchResult(type_, self.total, self.per_page, self.order, [result])
        b = SearchResult(type_, 10, self.per_page, 1, [result])
        c = SearchResult(type_, self.total, self.per_page, self.order, [result])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
