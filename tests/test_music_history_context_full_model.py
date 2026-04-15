from yandex_music import MusicHistoryContextFullModel


class TestMusicHistoryContextFullModel:
    available = True
    tracks_count = 335
    simple_wave_foreground_image_url = 'avatars.mds.yandex.net/get-music-misc/29541/img.64426e93aa320f4f1b4b6338/%%'
    simple_wave_background_color = '#2AA75B'

    def test_expected_value_album(self, music_history_context_full_model_album, album_without_tracks, artist):
        assert music_history_context_full_model_album.album == album_without_tracks
        assert music_history_context_full_model_album.artists == [artist]
        assert music_history_context_full_model_album.available == self.available

    def test_expected_value_artist(self, music_history_context_full_model_artist, artist):
        assert music_history_context_full_model_artist.artist == artist
        assert music_history_context_full_model_artist.available == self.available

    def test_de_json_none(self, client):
        assert MusicHistoryContextFullModel.de_json({}, client) is None

    def test_de_json_album(self, client, album_without_tracks, artist):
        json_dict = {
            'album': album_without_tracks.to_dict(),
            'artists': [artist.to_dict()],
            'available': self.available,
        }
        obj = MusicHistoryContextFullModel.de_json(json_dict, client)
        assert obj.album == album_without_tracks
        assert obj.artists == [artist]
        assert obj.available == self.available

    def test_de_json_artist(self, client, artist):
        json_dict = {
            'artist': artist.to_dict(),
            'available': self.available,
        }
        obj = MusicHistoryContextFullModel.de_json(json_dict, client)
        assert obj.artist == artist
        assert obj.available == self.available

    def test_equality(self, album_without_tracks):
        a = MusicHistoryContextFullModel(album=album_without_tracks)
        b = MusicHistoryContextFullModel(album=None)
        c = MusicHistoryContextFullModel(album=album_without_tracks)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
