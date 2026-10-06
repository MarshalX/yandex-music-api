from typing import Dict

import pytest

from yandex_music import Album, Client, JSONType, LabelAlbums, Pager


@pytest.fixture(scope='class')
def label_albums(album: Album, pager: Pager) -> LabelAlbums:
    return LabelAlbums([album], pager)


class TestLabelAlbums:
    def test_expected_values(self, label_albums: LabelAlbums, album: Album, pager: Pager) -> None:
        assert label_albums.albums == [album]
        assert label_albums.pager == pager

    def test_de_json_none(self, client: Client) -> None:
        assert LabelAlbums.de_json({}, client) is None

    def test_de_json_required(self, client: Client, album: Album, pager: Pager) -> None:
        json_dict: Dict[str, JSONType] = {'albums': [album.to_dict()], 'pager': pager.to_dict()}
        label_albums = LabelAlbums.de_json(json_dict, client)
        assert label_albums is not None

        assert label_albums.albums == [album]
        assert label_albums.pager == pager

    def test_de_json_all(self, client: Client, album: Album, pager: Pager) -> None:
        json_dict: Dict[str, JSONType] = {'albums': [album.to_dict()], 'pager': pager.to_dict()}
        label_albums = LabelAlbums.de_json(json_dict, client)
        assert label_albums is not None

        assert label_albums.albums == [album]
        assert label_albums.pager == pager

    def test_equality(self, album: Album, pager: Pager) -> None:
        a = LabelAlbums([album], pager)
        b = LabelAlbums([], pager)
        c = LabelAlbums([album], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, label_albums: LabelAlbums) -> None:
        assert len(label_albums) == len(label_albums.albums)

    def test_getitem(self, label_albums: LabelAlbums) -> None:
        assert label_albums[0] == label_albums.albums[0]

    def test_iter(self, label_albums: LabelAlbums) -> None:
        assert list(label_albums) == label_albums.albums
