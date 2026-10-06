from typing import Dict

import pytest

from yandex_music import ArtistTracks, Client, JSONType, Pager, Track


@pytest.fixture(scope='class')
def artist_tracks(track: Track, pager: Pager) -> ArtistTracks:
    return ArtistTracks([track], pager)


class TestArtistTracks:
    def test_expected_values(self, artist_tracks: ArtistTracks, track: Track, pager: Pager) -> None:
        assert artist_tracks.tracks == [track]
        assert artist_tracks.pager == pager

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistTracks.de_json({}, client) is None

    def test_de_json_required(self, client: Client, track: Track, pager: Pager) -> None:
        json_dict: Dict[str, JSONType] = {'tracks': [track.to_dict()], 'pager': pager.to_dict()}
        artist_tracks = ArtistTracks.de_json(json_dict, client)
        assert artist_tracks is not None

        assert artist_tracks.tracks == [track]
        assert artist_tracks.pager == pager

    def test_de_json_all(self, client: Client, track: Track, pager: Pager) -> None:
        json_dict: Dict[str, JSONType] = {'tracks': [track.to_dict()], 'pager': pager.to_dict()}
        artist_tracks = ArtistTracks.de_json(json_dict, client)
        assert artist_tracks is not None

        assert artist_tracks.tracks == [track]
        assert artist_tracks.pager == pager

    def test_equality(self, track: Track, pager: Pager) -> None:
        a = ArtistTracks([track], pager)
        b = ArtistTracks([], pager)
        c = ArtistTracks([track], pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, artist_tracks: ArtistTracks) -> None:
        assert len(artist_tracks) == len(artist_tracks.tracks)

    def test_getitem(self, artist_tracks: ArtistTracks) -> None:
        assert artist_tracks[0] == artist_tracks.tracks[0]

    def test_iter(self, artist_tracks: ArtistTracks) -> None:
        assert list(artist_tracks) == artist_tracks.tracks
