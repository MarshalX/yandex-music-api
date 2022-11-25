from yandex_music import LyricsInfo


class TestLyricsInfo:
    has_available_sync_lyrics = False
    has_available_text_lyrics = True

    def test_expected_values(self, lyrics_info):
        assert lyrics_info.has_available_sync_lyrics == self.has_available_sync_lyrics
        assert lyrics_info.has_available_text_lyrics == self.has_available_text_lyrics

    def test_de_json_none(self, client):
        assert LyricsInfo.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'has_available_sync_lyrics': self.has_available_sync_lyrics,
            'has_available_text_lyrics': self.has_available_text_lyrics,
        }
        lyrics_info = LyricsInfo.de_json(json_dict, client)

        assert lyrics_info.has_available_sync_lyrics == self.has_available_sync_lyrics
        assert lyrics_info.has_available_text_lyrics == self.has_available_text_lyrics

    def test_equality(self):
        a = LyricsInfo(self.has_available_sync_lyrics, self.has_available_text_lyrics)
        b = LyricsInfo(True, self.has_available_text_lyrics)
        c = LyricsInfo(self.has_available_sync_lyrics, self.has_available_text_lyrics)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
