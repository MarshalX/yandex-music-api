import pytest

from yandex_music import Search


@pytest.fixture(scope='class')
def search(best, albums, artists, playlists, tracks, videos):
    return Search(TestSearch.search_request_id, TestSearch.text, best, albums, artists, playlists, tracks, videos,
                  TestSearch.misspell_corrected, TestSearch.nocorrect)


class TestSearch:
    search_request_id = None
    text = None
    misspell_corrected = None
    nocorrect = None

    def test_expected_values(self, search, best, albums, artists, playlists, tracks, videos):
        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == albums
        assert search.artists == artists
        assert search.playlists == playlists
        assert search.tracks == tracks
        assert search.videos == videos
        assert search.misspell_corrected == self.misspell_corrected
        assert search.nocorrect == self.nocorrect

    def test_de_json_required(self, client, best, albums, artists, playlists, tracks, videos):
        json_dict = {'search_request_id': self.search_request_id, 'text': self.text, 'best': best, 'albums': albums,
                     'artists': artists, 'playlists': playlists, 'tracks': tracks, 'videos': videos}
        search = Search.de_json(json_dict, client)

        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == albums
        assert search.artists == artists
        assert search.playlists == playlists
        assert search.tracks == tracks
        assert search.videos == videos

    def test_de_json_all(self, client, best, albums, artists, playlists, tracks, videos):
        json_dict = {'search_request_id': self.search_request_id, 'text': self.text, 'best': best, 'albums': albums,
                     'artists': artists, 'playlists': playlists, 'tracks': tracks, 'videos': videos,
                     'misspell_corrected': self.misspell_corrected, 'nocorrect': self.nocorrect}
        search = Search.de_json(json_dict, client)

        assert search.search_request_id == self.search_request_id
        assert search.text == self.text
        assert search.best == best
        assert search.albums == albums
        assert search.artists == artists
        assert search.playlists == playlists
        assert search.tracks == tracks
        assert search.videos == videos
        assert search.misspell_corrected == self.misspell_corrected
        assert search.nocorrect == self.nocorrect

    def test_equality(self):
        pass
