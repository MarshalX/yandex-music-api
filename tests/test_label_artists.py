import pytest

from yandex_music import Artist, Client, LabelArtists, Pager


@pytest.fixture(scope='class')
def label_artists(artist: Artist, pager: Pager) -> LabelArtists:
    return LabelArtists([artist], pager)


class TestLabelArtists:
    def test_expected_values(self, label_artists: LabelArtists, artist: Artist, pager: Pager) -> None:
        assert label_artists.artists == [artist]
        assert label_artists.pager == pager

    def test_de_json_none(self, client: Client) -> None:
        assert LabelArtists.de_json({}, client) is None

    def test_de_json_required(self, client: Client, artist: Artist, pager: Pager) -> None:
        json_dict = {'artists': [artist.to_dict()], 'pager': pager.to_dict()}
        label_artists = LabelArtists.de_json(json_dict, client)
        assert label_artists is not None

        assert label_artists.artists == [artist]
        assert label_artists.pager == pager

    def test_de_json_all(self, client: Client, artist: Artist, pager: Pager) -> None:
        json_dict = {'artists': [artist.to_dict()], 'pager': pager.to_dict()}
        label_artists = LabelArtists.de_json(json_dict, client)
        assert label_artists is not None

        assert label_artists.artists == [artist]
        assert label_artists.pager == pager

    def test_equality(self, artist: Artist, pager: Pager) -> None:
        a = LabelArtists([artist], pager)
        b = LabelArtists([], pager)
        c = LabelArtists([artist], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, label_artists: LabelArtists) -> None:
        assert len(label_artists) == len(label_artists.artists)

    def test_getitem(self, label_artists: LabelArtists) -> None:
        assert label_artists[0] == label_artists.artists[0]

    def test_iter(self, label_artists: LabelArtists) -> None:
        assert list(label_artists) == label_artists.artists
