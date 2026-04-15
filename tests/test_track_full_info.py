from yandex_music import TrackFullInfo


class TestTrackFullInfo:
    aliases = ['alias1', 'alias2']

    def test_expected_value(self, track_full_info, track, artist):
        assert track_full_info.track == track
        assert track_full_info.similar_tracks == [track]
        assert track_full_info.also_in_albums == [track]
        assert track_full_info.aliases == self.aliases
        assert track_full_info.artists == [artist]

    def test_de_json_none(self, client):
        assert TrackFullInfo.de_json({}, client) is None

    def test_de_json_all(self, client, track, artist):
        json_dict = {
            'track': track.to_dict(),
            'similarTracks': [track.to_dict()],
            'alsoInAlbums': [track.to_dict()],
            'aliases': self.aliases,
            'artists': [artist.to_dict()],
        }
        track_full_info = TrackFullInfo.de_json(json_dict, client)

        assert track_full_info.track == track
        assert track_full_info.similar_tracks == [track]
        assert track_full_info.also_in_albums == [track]
        assert track_full_info.aliases == self.aliases
        assert track_full_info.artists == [artist]

    def test_equality(self, track):
        a = TrackFullInfo(track=track)
        b = TrackFullInfo(track=None)
        c = TrackFullInfo(track=track)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
