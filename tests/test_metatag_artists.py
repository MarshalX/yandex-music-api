import pytest

from yandex_music import MetatagArtists


@pytest.fixture(scope='class')
def metatag_artists_factory(metatag_artist_entry, pager, metatag_title, metatag_sort_by_value):
    def factory(**overrides):
        defaults = {
            'id': TestMetatagArtists.id,
            'cover_uri': TestMetatagArtists.cover_uri,
            'color': TestMetatagArtists.color,
            'title': metatag_title,
            'station_id': TestMetatagArtists.station_id,
            'pager': pager,
            'artists': [metatag_artist_entry],
            'sort_by_values': [metatag_sort_by_value],
        }
        defaults.update(overrides)
        return MetatagArtists(**defaults)

    return factory


class TestMetatagArtists:
    id = '5ddc2610e7c903105b40bc3a'
    cover_uri = 'avatars.yandex.net/get-music-misc/2406661/meta-tag.example.cover/%%'
    color = '#3779BC'
    station_id = 'genre:allrock'

    def test_expected_values(
        self,
        metatag_artists,
        metatag_artist_entry,
        pager,
        metatag_title,
        metatag_sort_by_value,
    ):
        assert metatag_artists.id == self.id
        assert metatag_artists.cover_uri == self.cover_uri
        assert metatag_artists.color == self.color
        assert metatag_artists.title == metatag_title
        assert metatag_artists.station_id == self.station_id
        assert metatag_artists.pager == pager
        assert metatag_artists.artists == [metatag_artist_entry]
        assert metatag_artists.sort_by_values == [metatag_sort_by_value]

    def test_de_json_none(self, client):
        assert MetatagArtists.de_json({}, client) is None

    def test_de_json_all(
        self,
        client,
        metatag_artist_entry,
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
            'artists': [metatag_artist_entry.to_dict()],
            'sortByValues': [metatag_sort_by_value.to_dict()],
        }
        metatag_artists = MetatagArtists.de_json(json_dict, client)

        assert metatag_artists.id == self.id
        assert metatag_artists.cover_uri == self.cover_uri
        assert metatag_artists.color == self.color
        assert metatag_artists.title == metatag_title
        assert metatag_artists.station_id == self.station_id
        assert metatag_artists.pager == pager
        assert metatag_artists.artists == [metatag_artist_entry]
        assert metatag_artists.sort_by_values == [metatag_sort_by_value]

    def test_equality(self, metatag_artists_factory):
        a = metatag_artists_factory()
        b = metatag_artists_factory(id='other')
        c = metatag_artists_factory()

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, metatag_artists):
        assert len(metatag_artists) == len(metatag_artists.artists)

    def test_getitem(self, metatag_artists):
        assert metatag_artists[0] == metatag_artists.artists[0]

    def test_iter(self, metatag_artists):
        assert list(metatag_artists) == metatag_artists.artists
