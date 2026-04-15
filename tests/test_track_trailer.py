from yandex_music import TrackTrailer


class TestTrackTrailer:
    title = 'Трейлер трека'

    def test_expected_value(self, track_trailer, track):
        assert track_trailer.title == self.title
        assert track_trailer.track == track

    def test_de_json_none(self, client):
        assert TrackTrailer.de_json({}, client) is None

    def test_de_json_all(self, client, track):
        json_dict = {
            'title': self.title,
            'track': track.to_dict(),
        }
        track_trailer = TrackTrailer.de_json(json_dict, client)

        assert track_trailer.title == self.title
        assert track_trailer.track == track

    def test_equality(self, track):
        a = TrackTrailer(title=self.title, track=track)
        b = TrackTrailer(title=None, track=track)
        c = TrackTrailer(title=self.title, track=track)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
