from yandex_music import Counts


class TestCounts:
    direct_albums = None
    also_tracks = None

    def test_expected_values(self, counts, tracks, also_albums):
        assert counts.tracks == tracks
        assert counts.direct_albums == self.direct_albums
        assert counts.also_albums == also_albums
        assert counts.also_tracks == self.also_tracks

    def test_de_json_required(self, client, tracks, also_albums):
        json_dict = {'tracks': tracks, 'direct_albums': self.direct_albums, 'also_albums': also_albums,
                     'also_tracks': self.also_tracks}
        counts = Counts.de_json(json_dict, client)

        assert counts.tracks == tracks
        assert counts.direct_albums == self.direct_albums
        assert counts.also_albums == also_albums
        assert counts.also_tracks == self.also_tracks

    def test_de_json_all(self, client, tracks, also_albums):
        json_dict = {'tracks': tracks, 'direct_albums': self.direct_albums, 'also_albums': also_albums,
                     'also_tracks': self.also_tracks}
        counts = Counts.de_json(json_dict, client)

        assert counts.tracks == tracks
        assert counts.direct_albums == self.direct_albums
        assert counts.also_albums == also_albums
        assert counts.also_tracks == self.also_tracks

    def test_equality(self):
        pass
