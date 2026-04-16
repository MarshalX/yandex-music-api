import pytest

from yandex_music import LabelAlbums


@pytest.fixture(scope='class')
def label_albums(album, pager):
    return LabelAlbums([album], pager)


class TestLabelAlbums:
    def test_expected_values(self, label_albums, album, pager):
        assert label_albums.albums == [album]
        assert label_albums.pager == pager

    def test_de_json_none(self, client):
        assert LabelAlbums.de_json({}, client) is None

    def test_de_json_required(self, client, album, pager):
        json_dict = {'albums': [album.to_dict()], 'pager': pager.to_dict()}
        label_albums = LabelAlbums.de_json(json_dict, client)

        assert label_albums.albums == [album]
        assert label_albums.pager == pager

    def test_de_json_all(self, client, album, pager):
        json_dict = {'albums': [album.to_dict()], 'pager': pager.to_dict()}
        label_albums = LabelAlbums.de_json(json_dict, client)

        assert label_albums.albums == [album]
        assert label_albums.pager == pager

    def test_equality(self, album, pager):
        a = LabelAlbums([album], pager)
        b = LabelAlbums([], pager)
        c = LabelAlbums([album], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, label_albums):
        assert len(label_albums) == len(label_albums.albums)

    def test_getitem(self, label_albums):
        assert label_albums[0] == label_albums.albums[0]

    def test_iter(self, label_albums):
        assert list(label_albums) == label_albums.albums
