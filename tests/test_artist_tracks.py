import pytest

from yandex_music import ArtistTracks


@pytest.fixture(scope='class')
def artist_tracks(track, pager):
    return ArtistTracks([track], pager)


class TestArtistTracks:
    def test_expected_values(self, artist_tracks, track, pager):
        assert artist_tracks.tracks == [track]
        assert artist_tracks.pager == pager

    def test_de_json_none(self, client):
        assert ArtistTracks.de_json({}, client) is None

    def test_de_json_required(self, client, track, pager):
        json_dict = {'tracks': [track.to_dict()], 'pager': pager.to_dict()}
        artist_tracks = ArtistTracks.de_json(json_dict, client)

        assert artist_tracks.tracks == [track]
        assert artist_tracks.pager == pager

    def test_de_json_all(self, client, track, pager):
        json_dict = {'tracks': [track.to_dict()], 'pager': pager.to_dict()}
        artist_tracks = ArtistTracks.de_json(json_dict, client)

        assert artist_tracks.tracks == [track]
        assert artist_tracks.pager == pager

    def test_equality(self, track, pager):
        a = ArtistTracks([track], pager)
        b = ArtistTracks([], pager)
        c = ArtistTracks([track], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, artist_tracks):
        assert len(artist_tracks) == len(artist_tracks.tracks)

    def test_getitem(self, artist_tracks):
        assert artist_tracks[0] == artist_tracks.tracks[0]

    def test_iter(self, artist_tracks):
        assert list(artist_tracks) == artist_tracks.tracks
