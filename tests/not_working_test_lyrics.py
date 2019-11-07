from yandex_music import Lyrics


class TestLyrics:
    full_lyrics = None
    has_rights = None
    text_language = None
    show_translation = None

    def test_expected_values(self, lyrics, id):
        assert lyrics.id == id
        assert lyrics.lyrics == lyrics
        assert lyrics.full_lyrics == self.full_lyrics
        assert lyrics.has_rights == self.has_rights
        assert lyrics.text_language == self.text_language
        assert lyrics.show_translation == self.show_translation

    def test_de_json_required(self, client, id):
        json_dict = {'id': id, 'lyrics': lyrics, 'full_lyrics': self.full_lyrics, 'has_rights': self.has_rights,
                     'text_language': self.text_language, 'show_translation': self.show_translation}
        lyrics = Lyrics.de_json(json_dict, client)

        assert lyrics.id == id
        assert lyrics.lyrics == lyrics
        assert lyrics.full_lyrics == self.full_lyrics
        assert lyrics.has_rights == self.has_rights
        assert lyrics.text_language == self.text_language
        assert lyrics.show_translation == self.show_translation

    def test_de_json_all(self, client, id):
        json_dict = {'id': id, 'lyrics': lyrics, 'full_lyrics': self.full_lyrics, 'has_rights': self.has_rights,
                     'text_language': self.text_language, 'show_translation': self.show_translation}
        lyrics = Lyrics.de_json(json_dict, client)

        assert lyrics.id == id
        assert lyrics.lyrics == lyrics
        assert lyrics.full_lyrics == self.full_lyrics
        assert lyrics.has_rights == self.has_rights
        assert lyrics.text_language == self.text_language
        assert lyrics.show_translation == self.show_translation

    def test_equality(self):
        pass
