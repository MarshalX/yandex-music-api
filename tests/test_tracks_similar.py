from typing import Dict

import pytest

from yandex_music import Client, JSONType, SimilarTracks, Track


@pytest.fixture(scope='class')
def similar_tracks(track: Track) -> SimilarTracks:
    return SimilarTracks(track, [track])


class TestSimilarTracks:
    def test_expected_values(self, similar_tracks: SimilarTracks, track: Track) -> None:
        assert similar_tracks.track == track
        assert similar_tracks.similar_tracks == [track]

    def test_de_json_none(self, client: Client) -> None:
        assert SimilarTracks.de_json({}, client) is None

    def test_de_json_required(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'track': track.to_dict(), 'similar_tracks': [track.to_dict()]}
        similar_tracks = SimilarTracks.de_json(json_dict, client)
        assert similar_tracks is not None

        assert similar_tracks.track == track
        assert similar_tracks.similar_tracks == [track]

    def test_de_json_all(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'track': track.to_dict(), 'similar_tracks': [track.to_dict()]}
        similar_tracks = SimilarTracks.de_json(json_dict, client)
        assert similar_tracks is not None

        assert similar_tracks.track == track
        assert similar_tracks.similar_tracks == [track]

    def test_equality(self, track: Track) -> None:
        a = SimilarTracks(track, [track])
        b = SimilarTracks(None, [track])
        c = SimilarTracks(track, [track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_len(self, similar_tracks: SimilarTracks) -> None:
        assert len(similar_tracks) == len(similar_tracks.similar_tracks)

    def test_getitem(self, similar_tracks: SimilarTracks) -> None:
        assert similar_tracks[0] == similar_tracks.similar_tracks[0]

    def test_iter(self, similar_tracks: SimilarTracks) -> None:
        assert list(similar_tracks) == similar_tracks.similar_tracks
