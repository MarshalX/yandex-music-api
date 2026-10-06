from typing import Callable, Dict

import pytest

from yandex_music import Client, JSONType, MetatagPlaylists, MetatagSortByValue, MetatagTitle, Pager, Playlist


@pytest.fixture(scope='class')
def metatag_playlists_factory(
    playlist: Playlist, pager: Pager, metatag_title: MetatagTitle, metatag_sort_by_value: MetatagSortByValue
) -> Callable[..., MetatagPlaylists]:
    def factory(id_: str = TestMetatagPlaylists.id) -> MetatagPlaylists:
        return MetatagPlaylists(
            id=id_,
            cover_uri=TestMetatagPlaylists.cover_uri,
            color=TestMetatagPlaylists.color,
            title=metatag_title,
            station_id=TestMetatagPlaylists.station_id,
            pager=pager,
            playlists=[playlist],
            sort_by_values=[metatag_sort_by_value],
        )

    return factory


class TestMetatagPlaylists:
    id = '5ddc2610e7c903105b40bc3a'
    cover_uri = 'avatars.yandex.net/get-music-misc/2406661/meta-tag.example.cover/%%'
    color = '#3779BC'
    station_id = 'genre:allrock'

    def test_expected_values(
        self,
        metatag_playlists: MetatagPlaylists,
        playlist: Playlist,
        pager: Pager,
        metatag_title: MetatagTitle,
        metatag_sort_by_value: MetatagSortByValue,
    ) -> None:
        assert metatag_playlists.id == self.id
        assert metatag_playlists.cover_uri == self.cover_uri
        assert metatag_playlists.color == self.color
        assert metatag_playlists.title == metatag_title
        assert metatag_playlists.station_id == self.station_id
        assert metatag_playlists.pager == pager
        assert metatag_playlists.playlists == [playlist]
        assert metatag_playlists.sort_by_values == [metatag_sort_by_value]

    def test_de_json_none(self, client: Client) -> None:
        assert MetatagPlaylists.de_json({}, client) is None

    def test_de_json_all(
        self,
        client: Client,
        playlist: Playlist,
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
            'playlists': [playlist.to_dict()],
            'sortByValues': [metatag_sort_by_value.to_dict()],
        }
        metatag_playlists = MetatagPlaylists.de_json(json_dict, client)
        assert metatag_playlists is not None

        assert metatag_playlists.id == self.id
        assert metatag_playlists.cover_uri == self.cover_uri
        assert metatag_playlists.color == self.color
        assert metatag_playlists.title == metatag_title
        assert metatag_playlists.station_id == self.station_id
        assert metatag_playlists.pager == pager
        assert metatag_playlists.playlists == [playlist]
        assert metatag_playlists.sort_by_values == [metatag_sort_by_value]

    def test_equality(self, metatag_playlists_factory: Callable[..., MetatagPlaylists]) -> None:
        a = metatag_playlists_factory()
        b = metatag_playlists_factory(id_='other')
        c = metatag_playlists_factory()

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, metatag_playlists: MetatagPlaylists) -> None:
        assert len(metatag_playlists) == len(metatag_playlists.playlists)

    def test_getitem(self, metatag_playlists: MetatagPlaylists) -> None:
        assert metatag_playlists[0] == metatag_playlists.playlists[0]

    def test_iter(self, metatag_playlists: MetatagPlaylists) -> None:
        assert list(metatag_playlists) == metatag_playlists.playlists
