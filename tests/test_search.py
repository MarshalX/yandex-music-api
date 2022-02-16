import pytest

from tests import TestSearchResult
from yandex_music import Search, SearchResult


@pytest.fixture(scope='class')
def search_result(results, types):
    def make_search_result(param):
        return SearchResult(
            types[param], TestSearchResult.total, TestSearchResult.per_page, TestSearchResult.order, [results[param]]
        )

    return make_search_result


@pytest.fixture(scope='class')
def search(best, search_result):
    return Search(
        TestSearch.search_request_id,
        TestSearch.text,
        best,
        search_result(3),
        search_result(2),
        search_result(4),
        search_result(1),
        search_result(5),
        search_result(13),
        search_result(14),
        search_result(15),
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

    def test_expected_values(self, search, best, search_result):
        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == search_result(3)
        assert search.artists == search_result(2)
        assert search.playlists == search_result(4)
        assert search.tracks == search_result(1)
        assert search.videos == search_result(5)
        assert search.users == search_result(13)
        assert search.podcasts == search_result(14)
        assert search.podcast_episodes == search_result(15)
        assert search.type == self.type_
        assert search.page == self.page
        assert search.per_page == self.per_page
        assert search.misspell_result == self.misspell_result
        assert search.misspell_original == self.misspell_original
        assert search.misspell_corrected == self.misspell_corrected
        assert search.nocorrect == self.nocorrect

    def test_de_json_none(self, client):
        assert Search.de_json({}, client) is None

    def test_de_json_required(self, client, best, search_result):
        json_dict = {
            'search_request_id': self.search_request_id,
            'text': self.text,
            'best': best.to_dict(),
            'albums': search_result(3).to_dict(),
            'artists': search_result(2).to_dict(),
            'playlists': search_result(4).to_dict(),
            'tracks': search_result(1).to_dict(),
            'videos': search_result(5).to_dict(),
            'users': search_result(13).to_dict(),
            'podcasts': search_result(14).to_dict(),
            'podcast_episodes': search_result(15).to_dict(),
        }
        search = Search.de_json(json_dict, client)

        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == search_result(3)
        assert search.artists == search_result(2)
        assert search.playlists == search_result(4)
        assert search.tracks == search_result(1)
        assert search.videos == search_result(5)
        assert search.users == search_result(13)
        assert search.podcasts == search_result(14)
        assert search.podcast_episodes == search_result(15)

    def test_de_json_all(self, client, best, search_result):
        json_dict = {
            'search_request_id': self.search_request_id,
            'text': self.text,
            'best': best.to_dict(),
            'albums': search_result(3).to_dict(),
            'artists': search_result(2).to_dict(),
            'playlists': search_result(4).to_dict(),
            'tracks': search_result(1).to_dict(),
            'videos': search_result(5).to_dict(),
            'users': search_result(13).to_dict(),
            'podcasts': search_result(14).to_dict(),
            'podcast_episodes': search_result(15).to_dict(),
            'misspell_corrected': self.misspell_corrected,
            'nocorrect': self.nocorrect,
            'type': self.type_,
            'page': self.page,
            'per_page': self.per_page,
            'misspell_result': self.misspell_result,
            'misspell_original': self.misspell_original,
        }
        search = Search.de_json(json_dict, client)

        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == search_result(3)
        assert search.artists == search_result(2)
        assert search.playlists == search_result(4)
        assert search.tracks == search_result(1)
        assert search.videos == search_result(5)
        assert search.users == search_result(13)
        assert search.podcasts == search_result(14)
        assert search.podcast_episodes == search_result(15)
        assert search.type == self.type_
        assert search.page == self.page
        assert search.per_page == self.per_page
        assert search.misspell_result == self.misspell_result
        assert search.misspell_original == self.misspell_original
        assert search.misspell_corrected == self.misspell_corrected
        assert search.nocorrect == self.nocorrect

    def test_equality(self, best, search_result):
        a = Search(
            self.search_request_id,
            self.text,
            best,
            search_result(3),
            search_result(2),
            search_result(4),
            search_result(1),
            search_result(5),
            search_result(13),
            search_result(14),
            search_result(15),
        )
        b = Search(
            self.search_request_id,
            '',
            best,
            search_result(3),
            None,
            search_result(4),
            search_result(1),
            search_result(5),
            search_result(13),
            None,
            search_result(15),
        )
        c = Search(
            self.search_request_id,
            self.text,
            best,
            search_result(3),
            search_result(2),
            search_result(4),
            search_result(1),
            search_result(5),
            search_result(13),
            search_result(14),
            search_result(15),
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
