from yandex_music import Counts


class TestCounts:
    tracks = 94
    direct_albums = 9
    also_albums = 0
    also_tracks = 0

    def test_expected_values(self, counts):
        assert counts.tracks == self.tracks
        assert counts.direct_albums == self.direct_albums
        assert counts.also_albums == self.also_albums
        assert counts.also_tracks == self.also_tracks

    def test_de_json_none(self, client):
        assert Counts.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'tracks': self.tracks,
            'direct_albums': self.direct_albums,
            'also_albums': self.also_albums,
            'also_tracks': self.also_tracks,
        }
        counts = Counts.de_json(json_dict, client)

        assert counts.tracks == self.tracks
        assert counts.direct_albums == self.direct_albums
        assert counts.also_albums == self.also_albums
        assert counts.also_tracks == self.also_tracks

    def test_de_json_all(self, client):
        json_dict = {
            'tracks': self.tracks,
            'direct_albums': self.direct_albums,
            'also_albums': self.also_albums,
            'also_tracks': self.also_tracks,
        }
        counts = Counts.de_json(json_dict, client)

        assert counts.tracks == self.tracks
        assert counts.direct_albums == self.direct_albums
        assert counts.also_albums == self.also_albums
        assert counts.also_tracks == self.also_tracks

    def test_equality(self):
        a = Counts(self.tracks, self.direct_albums, self.also_albums, self.also_tracks)
        b = Counts(40, self.direct_albums, 30, self.also_tracks)
        c = Counts(self.tracks, self.direct_albums, 10, 10)
        d = Counts(self.tracks, self.direct_albums, self.also_albums, self.also_tracks)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
