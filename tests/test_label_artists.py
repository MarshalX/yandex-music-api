import pytest

from yandex_music import LabelArtists


@pytest.fixture(scope='class')
def label_artists(artist, pager):
    return LabelArtists([artist], pager)


class TestLabelArtists:
    def test_expected_values(self, label_artists, artist, pager):
        assert label_artists.artists == [artist]
        assert label_artists.pager == pager

    def test_de_json_none(self, client):
        assert LabelArtists.de_json({}, client) is None

    def test_de_json_required(self, client, artist, pager):
        json_dict = {'artists': [artist.to_dict()], 'pager': pager.to_dict()}
        label_artists = LabelArtists.de_json(json_dict, client)

        assert label_artists.artists == [artist]
        assert label_artists.pager == pager

    def test_de_json_all(self, client, artist, pager):
        json_dict = {'artists': [artist.to_dict()], 'pager': pager.to_dict()}
        label_artists = LabelArtists.de_json(json_dict, client)

        assert label_artists.artists == [artist]
        assert label_artists.pager == pager

    def test_equality(self, artist, pager):
        a = LabelArtists([artist], pager)
        b = LabelArtists([], pager)
        c = LabelArtists([artist], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, label_artists):
        assert len(label_artists) == len(label_artists.artists)

    def test_getitem(self, label_artists):
        assert label_artists[0] == label_artists.artists[0]

    def test_iter(self, label_artists):
        assert list(label_artists) == label_artists.artists
