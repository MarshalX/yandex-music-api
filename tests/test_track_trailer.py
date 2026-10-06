from typing import Dict

from yandex_music import Client, JSONType, Track, TrackTrailer


class TestTrackTrailer:
    title = 'Трейлер трека'

    def test_expected_value(self, track_trailer: TrackTrailer, track: Track) -> None:
        assert track_trailer.title == self.title
        assert track_trailer.track == track

    def test_de_json_none(self, client: Client) -> None:
        assert TrackTrailer.de_json({}, client) is None

    def test_de_json_all(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'track': track.to_dict(),
        }
        track_trailer = TrackTrailer.de_json(json_dict, client)
        assert track_trailer is not None

        assert track_trailer.title == self.title
        assert track_trailer.track == track

    def test_equality(self, track: Track) -> None:
        a = TrackTrailer(title=self.title, track=track)
        b = TrackTrailer(title=None, track=track)
        c = TrackTrailer(title=self.title, track=track)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
