from typing import Callable, Dict

import pytest

from yandex_music import Client, JSONType, MetatagArtistEntry, MetatagArtists, MetatagSortByValue, MetatagTitle, Pager


@pytest.fixture(scope='class')
def metatag_artists_factory(
    metatag_artist_entry: MetatagArtistEntry,
    pager: Pager,
    metatag_title: MetatagTitle,
    metatag_sort_by_value: MetatagSortByValue,
) -> Callable[..., MetatagArtists]:
    def factory(id: str = TestMetatagArtists.id) -> MetatagArtists:
        return MetatagArtists(
            id=id,
            cover_uri=TestMetatagArtists.cover_uri,
            color=TestMetatagArtists.color,
            title=metatag_title,
            station_id=TestMetatagArtists.station_id,
            pager=pager,
            artists=[metatag_artist_entry],
            sort_by_values=[metatag_sort_by_value],
        )

    return factory


class TestMetatagArtists:
    id = '5ddc2610e7c903105b40bc3a'
    cover_uri = 'avatars.yandex.net/get-music-misc/2406661/meta-tag.example.cover/%%'
    color = '#3779BC'
    station_id = 'genre:allrock'

    def test_expected_values(
        self,
        metatag_artists: MetatagArtists,
        metatag_artist_entry: MetatagArtistEntry,
        pager: Pager,
        metatag_title: MetatagTitle,
        metatag_sort_by_value: MetatagSortByValue,
    ) -> None:
        assert metatag_artists.id == self.id
        assert metatag_artists.cover_uri == self.cover_uri
        assert metatag_artists.color == self.color
        assert metatag_artists.title == metatag_title
        assert metatag_artists.station_id == self.station_id
        assert metatag_artists.pager == pager
        assert metatag_artists.artists == [metatag_artist_entry]
        assert metatag_artists.sort_by_values == [metatag_sort_by_value]

    def test_de_json_none(self, client: Client) -> None:
        assert MetatagArtists.de_json({}, client) is None

    def test_de_json_all(
        self,
        client: Client,
        metatag_artist_entry: MetatagArtistEntry,
        pager: Pager,
        metatag_title: MetatagTitle,
        metatag_sort_by_value: MetatagSortByValue,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
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
        assert metatag_artists is not None

        assert metatag_artists.id == self.id
        assert metatag_artists.cover_uri == self.cover_uri
        assert metatag_artists.color == self.color
        assert metatag_artists.title == metatag_title
        assert metatag_artists.station_id == self.station_id
        assert metatag_artists.pager == pager
        assert metatag_artists.artists == [metatag_artist_entry]
        assert metatag_artists.sort_by_values == [metatag_sort_by_value]

    def test_equality(self, metatag_artists_factory: Callable[..., MetatagArtists]) -> None:
        a = metatag_artists_factory()
        b = metatag_artists_factory(id='other')
        c = metatag_artists_factory()

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, metatag_artists: MetatagArtists) -> None:
        assert len(metatag_artists) == len(metatag_artists.artists)

    def test_getitem(self, metatag_artists: MetatagArtists) -> None:
        assert metatag_artists[0] == metatag_artists.artists[0]

    def test_iter(self, metatag_artists: MetatagArtists) -> None:
        assert list(metatag_artists) == metatag_artists.artists
