import pytest

from yandex_music import ArtistAlbums


@pytest.fixture(scope='class')
def artist_albums(album, pager):
    return ArtistAlbums([album], pager)


class TestArtistAlbums:
    def test_expected_values(self, artist_albums, album, pager):
        assert artist_albums.albums == [album]
        assert artist_albums.pager == pager

    def test_de_json_none(self, client):
        assert ArtistAlbums.de_json({}, client) is None

    def test_de_json_required(self, client, album, pager):
        json_dict = {'albums': [album.to_dict()], 'pager': pager.to_dict()}
        artist_albums = ArtistAlbums.de_json(json_dict, client)

        assert artist_albums.albums == [album]
        assert artist_albums.pager == pager

    def test_de_json_all(self, client, album, pager):
        json_dict = {'albums': [album.to_dict()], 'pager': pager.to_dict()}
        artist_albums = ArtistAlbums.de_json(json_dict, client)

        assert artist_albums.albums == [album]
        assert artist_albums.pager == pager

    def test_equality(self, album, pager):
        a = ArtistAlbums([album], pager)
        b = ArtistAlbums([], pager)
        c = ArtistAlbums([album], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, artist_albums):
        assert len(artist_albums) == len(artist_albums.albums)

    def test_getitem(self, artist_albums):
        assert artist_albums[0] == artist_albums.albums[0]

    def test_iter(self, artist_albums):
        assert list(artist_albums) == artist_albums.albums
