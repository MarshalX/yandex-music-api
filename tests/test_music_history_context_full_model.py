from typing import Dict

from yandex_music import Album, Artist, Client, JSONType, MusicHistoryContextFullModel


class TestMusicHistoryContextFullModel:
    available = True
    tracks_count = 335
    simple_wave_foreground_image_url = 'avatars.mds.yandex.net/get-music-misc/29541/img.64426e93aa320f4f1b4b6338/%%'
    simple_wave_background_color = '#2AA75B'

    def test_expected_value_album(
        self,
        music_history_context_full_model_album: MusicHistoryContextFullModel,
        album_without_tracks: Album,
        artist: Artist,
    ) -> None:
        assert music_history_context_full_model_album.album == album_without_tracks
        assert music_history_context_full_model_album.artists == [artist]
        assert music_history_context_full_model_album.available == self.available

    def test_expected_value_artist(
        self, music_history_context_full_model_artist: MusicHistoryContextFullModel, artist: Artist
    ) -> None:
        assert music_history_context_full_model_artist.artist == artist
        assert music_history_context_full_model_artist.available == self.available

    def test_de_json_none(self, client: Client) -> None:
        assert MusicHistoryContextFullModel.de_json({}, client) is None

    def test_de_json_album(self, client: Client, album_without_tracks: Album, artist: Artist) -> None:
        json_dict: Dict[str, JSONType] = {
            'album': album_without_tracks.to_dict(),
            'artists': [artist.to_dict()],
            'available': self.available,
        }
        obj = MusicHistoryContextFullModel.de_json(json_dict, client)
        assert obj is not None
        assert obj.album == album_without_tracks
        assert obj.artists == [artist]
        assert obj.available == self.available

    def test_de_json_artist(self, client: Client, artist: Artist) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'available': self.available,
        }
        obj = MusicHistoryContextFullModel.de_json(json_dict, client)
        assert obj is not None
        assert obj.artist == artist
        assert obj.available == self.available

    def test_equality(self, album_without_tracks: Album) -> None:
        a = MusicHistoryContextFullModel(album=album_without_tracks)
        b = MusicHistoryContextFullModel(album=None)
        c = MusicHistoryContextFullModel(album=album_without_tracks)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
