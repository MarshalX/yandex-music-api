import pytest

from yandex_music import MetatagAlbums


@pytest.fixture(scope='class')
def metatag_albums_factory(album, pager, metatag_title, metatag_sort_by_value):
    def factory(**overrides):
        defaults = {
            'id': TestMetatagAlbums.id,
            'cover_uri': TestMetatagAlbums.cover_uri,
            'color': TestMetatagAlbums.color,
            'title': metatag_title,
            'station_id': TestMetatagAlbums.station_id,
            'pager': pager,
            'albums': [album],
            'sort_by_values': [metatag_sort_by_value],
        }
        defaults.update(overrides)
        return MetatagAlbums(**defaults)

    return factory


class TestMetatagAlbums:
    id = '5ddc2610e7c903105b40bc3a'
    cover_uri = 'avatars.yandex.net/get-music-misc/2406661/meta-tag.example.cover/%%'
    color = '#3779BC'
    station_id = 'genre:allrock'

    def test_expected_values(
        self,
        metatag_albums,
        album,
        pager,
        metatag_title,
        metatag_sort_by_value,
    ):
        assert metatag_albums.id == self.id
        assert metatag_albums.cover_uri == self.cover_uri
        assert metatag_albums.color == self.color
        assert metatag_albums.title == metatag_title
        assert metatag_albums.station_id == self.station_id
        assert metatag_albums.pager == pager
        assert metatag_albums.albums == [album]
        assert metatag_albums.sort_by_values == [metatag_sort_by_value]

    def test_de_json_none(self, client):
        assert MetatagAlbums.de_json({}, client) is None

    def test_de_json_all(
        self,
        client,
        album,
        pager,
        metatag_title,
        metatag_sort_by_value,
    ):
        json_dict = {
            'id': self.id,
            'coverUri': self.cover_uri,
            'color': self.color,
            'title': metatag_title.to_dict(),
            'stationId': self.station_id,
            'pager': pager.to_dict(),
            'albums': [album.to_dict()],
            'sortByValues': [metatag_sort_by_value.to_dict()],
        }
        metatag_albums = MetatagAlbums.de_json(json_dict, client)

        assert metatag_albums.id == self.id
        assert metatag_albums.cover_uri == self.cover_uri
        assert metatag_albums.color == self.color
        assert metatag_albums.title == metatag_title
        assert metatag_albums.station_id == self.station_id
        assert metatag_albums.pager == pager
        assert metatag_albums.albums == [album]
        assert metatag_albums.sort_by_values == [metatag_sort_by_value]

    def test_equality(self, metatag_albums_factory):
        a = metatag_albums_factory()
        b = metatag_albums_factory(id='other')
        c = metatag_albums_factory()

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, metatag_albums):
        assert len(metatag_albums) == len(metatag_albums.albums)

    def test_getitem(self, metatag_albums):
        assert metatag_albums[0] == metatag_albums.albums[0]

    def test_iter(self, metatag_albums):
        assert list(metatag_albums) == metatag_albums.albums
