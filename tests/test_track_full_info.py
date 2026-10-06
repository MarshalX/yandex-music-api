from typing import Dict

from yandex_music import Artist, Client, JSONType, Track, TrackFullInfo


class TestTrackFullInfo:
    aliases = ['alias1', 'alias2']

    def test_expected_value(self, track_full_info: TrackFullInfo, track: Track, artist: Artist) -> None:
        assert track_full_info.track == track
        assert track_full_info.similar_tracks == [track]
        assert track_full_info.also_in_albums == [track]
        assert track_full_info.aliases == self.aliases
        assert track_full_info.artists == [artist]

    def test_de_json_none(self, client: Client) -> None:
        assert TrackFullInfo.de_json({}, client) is None

    def test_de_json_all(self, client: Client, track: Track, artist: Artist) -> None:
        json_dict: Dict[str, JSONType] = {
            'track': track.to_dict(),
            'similarTracks': [track.to_dict()],
            'alsoInAlbums': [track.to_dict()],
            'aliases': self.aliases,
            'artists': [artist.to_dict()],
        }
        track_full_info = TrackFullInfo.de_json(json_dict, client)
        assert track_full_info is not None

        assert track_full_info.track == track
        assert track_full_info.similar_tracks == [track]
        assert track_full_info.also_in_albums == [track]
        assert track_full_info.aliases == self.aliases
        assert track_full_info.artists == [artist]

    def test_equality(self, track: Track) -> None:
        a = TrackFullInfo(track=track)
        b = TrackFullInfo(track=None)
        c = TrackFullInfo(track=track)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
