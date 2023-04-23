from yandex_music.utils.convert_track_id import convert_track_id_to_number


class TestConvertTrackId:
    track_id = 37696396
    album_id = 4784420

    def test_convert_from_str(self):
        assert convert_track_id_to_number(f'{self.track_id}:{self.album_id}') == self.track_id
        assert convert_track_id_to_number(f'{self.track_id}:') == self.track_id
        assert convert_track_id_to_number(f'{self.track_id}') == self.track_id

    def test_convert_from_int(self):
        assert convert_track_id_to_number(self.track_id) == self.track_id
