from typing import Dict, Mapping, Type, TypeVar, Union

import pytest

from tests import TestSearchResult
from yandex_music import Album, Artist, Best, Client, JSONType, Playlist, Search, SearchResult, Track, User, Video

T = TypeVar('T', bound=Union[Track, Artist, Album, Playlist, Video, User])


class SearchResultFactory:
    def __init__(self, results: Mapping[int, object], types: Dict[int, str]) -> None:
        self.results = results
        self.types = types

    def __call__(self, param: int, item_type: Type[T]) -> SearchResult[T]:
        result = self.results[param]
        assert isinstance(result, item_type)
        return SearchResult(
            self.types[param], TestSearchResult.total, TestSearchResult.per_page, TestSearchResult.order, [result]
        )


@pytest.fixture(scope='class')
def search_result(results: Mapping[int, object], types: Dict[int, str]) -> SearchResultFactory:
    return SearchResultFactory(results, types)


@pytest.fixture(scope='class')
def search(best: Best, search_result: SearchResultFactory) -> Search:
    return Search(
        TestSearch.search_request_id,
        TestSearch.text,
        best,
        search_result(3, Album),
        search_result(2, Artist),
        search_result(4, Playlist),
        search_result(1, Track),
        search_result(5, Video),
        search_result(13, User),
        search_result(14, Album),
        search_result(15, Track),
        TestSearch.type_,
        TestSearch.page,
        TestSearch.per_page,
        TestSearch.misspell_result,
        TestSearch.misspell_original,
        TestSearch.misspell_corrected,
        TestSearch.nocorrect,
    )


class TestSearch:
    search_request_id = (
        'myt1-0261-c2e-msk-myt-music-st-e72-18274.gencfg-c.yandex.net-1573323135801461'
        '-3742331365077765411-1573323135819 '
    )
    text = 'NCS'
    type_ = 'artist'
    page = 0
    per_page = 10
    misspell_result = 'era ameno'
    misspell_original = 'ero amen'
    misspell_corrected = False
    nocorrect = False

    def test_expected_values(self, search: Search, best: Best, search_result: SearchResultFactory) -> None:
        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == search_result(3, Album)
        assert search.artists == search_result(2, Artist)
        assert search.playlists == search_result(4, Playlist)
        assert search.tracks == search_result(1, Track)
        assert search.videos == search_result(5, Video)
        assert search.users == search_result(13, User)
        assert search.podcasts == search_result(14, Album)
        assert search.podcast_episodes == search_result(15, Track)
        assert search.type == self.type_
        assert search.page == self.page
        assert search.per_page == self.per_page
        assert search.misspell_result == self.misspell_result
        assert search.misspell_original == self.misspell_original
        assert search.misspell_corrected == self.misspell_corrected
        assert search.nocorrect == self.nocorrect

    def test_de_json_none(self, client: Client) -> None:
        assert Search.de_json({}, client) is None

    def test_de_json_required(self, client: Client, best: Best, search_result: SearchResultFactory) -> None:
        json_dict: Dict[str, JSONType] = {
            'search_request_id': self.search_request_id,
            'text': self.text,
            'best': best.to_dict(),
            'albums': search_result(3, Album).to_dict(),
            'artists': search_result(2, Artist).to_dict(),
            'playlists': search_result(4, Playlist).to_dict(),
            'tracks': search_result(1, Track).to_dict(),
            'videos': search_result(5, Video).to_dict(),
            'users': search_result(13, User).to_dict(),
            'podcasts': search_result(14, Album).to_dict(),
            'podcast_episodes': search_result(15, Track).to_dict(),
        }
        search = Search.de_json(json_dict, client)
        assert search is not None

        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == search_result(3, Album)
        assert search.artists == search_result(2, Artist)
        assert search.playlists == search_result(4, Playlist)
        assert search.tracks == search_result(1, Track)
        assert search.videos == search_result(5, Video)
        assert search.users == search_result(13, User)
        assert search.podcasts == search_result(14, Album)
        assert search.podcast_episodes == search_result(15, Track)

    def test_de_json_all(self, client: Client, best: Best, search_result: SearchResultFactory) -> None:
        json_dict: Dict[str, JSONType] = {
            'search_request_id': self.search_request_id,
            'text': self.text,
            'best': best.to_dict(),
            'albums': search_result(3, Album).to_dict(),
            'artists': search_result(2, Artist).to_dict(),
            'playlists': search_result(4, Playlist).to_dict(),
            'tracks': search_result(1, Track).to_dict(),
            'videos': search_result(5, Video).to_dict(),
            'users': search_result(13, User).to_dict(),
            'podcasts': search_result(14, Album).to_dict(),
            'podcast_episodes': search_result(15, Track).to_dict(),
            'misspell_corrected': self.misspell_corrected,
            'nocorrect': self.nocorrect,
            'type': self.type_,
            'page': self.page,
            'per_page': self.per_page,
            'misspell_result': self.misspell_result,
            'misspell_original': self.misspell_original,
        }
        search = Search.de_json(json_dict, client)
        assert search is not None

        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == search_result(3, Album)
        assert search.artists == search_result(2, Artist)
        assert search.playlists == search_result(4, Playlist)
        assert search.tracks == search_result(1, Track)
        assert search.videos == search_result(5, Video)
        assert search.users == search_result(13, User)
        assert search.podcasts == search_result(14, Album)
        assert search.podcast_episodes == search_result(15, Track)
        assert search.type == self.type_
        assert search.page == self.page
        assert search.per_page == self.per_page
        assert search.misspell_result == self.misspell_result
        assert search.misspell_original == self.misspell_original
        assert search.misspell_corrected == self.misspell_corrected
        assert search.nocorrect == self.nocorrect

    def test_equality(self, best: Best, search_result: SearchResultFactory) -> None:
        a = Search(
            self.search_request_id,
            self.text,
            best,
            search_result(3, Album),
            search_result(2, Artist),
            search_result(4, Playlist),
            search_result(1, Track),
            search_result(5, Video),
            search_result(13, User),
            search_result(14, Album),
            search_result(15, Track),
        )
        b = Search(
            self.search_request_id,
            '',
            best,
            search_result(3, Album),
            None,
            search_result(4, Playlist),
            search_result(1, Track),
            search_result(5, Video),
            search_result(13, User),
            None,
            search_result(15, Track),
        )
        c = Search(
            self.search_request_id,
            self.text,
            best,
            search_result(3, Album),
            search_result(2, Artist),
            search_result(4, Playlist),
            search_result(1, Track),
            search_result(5, Video),
            search_result(13, User),
            search_result(14, Album),
            search_result(15, Track),
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
