from yandex_music import Lyrics


class TestLyrics:
    id = 103844
    lyrics = 'Too big, too small?\nSize does matter, after all\nZu groß, zu klein?\nEr könnte etwas größer sein'
    full_lyrics = (
        'Too big, too small?\nSize does matter, after all\nZu groß, zu klein?\nEr könnte etwas größer '
        'sein\n\nMercedes-Benz und Autobahn\nAlleine in das Ausland fahren\nReise, '
        'Reise! Fahrvergnügen\nIch will nur Spaß, mich nicht verlieben\n\nJust a little bit...\nJust a '
        'little, bitch!\n\nYou\'ve got a pussy\nI have a dick, ah.\nSo what\'s the problem?\nLet\'s do it '
        'quick!\n\nSo take me now, before it\'s too late\nLife\'s too short, so I can\'t wait\nTake me now! '
        'Oh, don\'t you see?\nI can\'t get laid in Germany…\n\nToo short, too tall?\nDoesn\'t matter, '
        'one size fits all\nZu groß, zu klein?\nDer Schlagbaum sollte oben sein\n\nSchönes Fräulein, '
        'Lust auf mehr\nBlitzkrieg mit dem Fleischgewehr\nSchnaps im Kopf, du holde Braut\nSteck Bratwurst '
        'in dein Sauerkraut\n\nJust a little bit...\nBe my little bitch!\n\nYou\'ve got a pussy\nI have a '
        'dick, ah\nSo what\'s the problem?\nLet\'s do it quick!\n\nSo take me now, before it\'s too '
        'late\nLife\'s too short, so I can\'t wait\nTake me now! Oh, don\'t you see?\nI can\'t get laid in '
        'Germany…\n\nGermany! Germany!\n\nYou\'ve got a pussy\nI have a dick, ah\nSo what\'s the '
        'problem?\nLet\'s do it quick!\n\nYou\'ve got a pussy\nI have a dick, ah\nSo what\'s the '
        'problem?\nLet\'s do it quick!\n\nYou\'ve got a pussy\nI have a dick, ah\nSo what\'s the '
        'problem?\nLet\'s do it quick!\n\nSo take me now, before it\'s too late\nLife\'s too short, '
        'so I can\'t wait\nTake me now! Oh, don\'t you see?\nI can\'t get laid in Germany…\n '
    )
    has_rights = True
    text_language = 'de'
    show_translation = True
    url = 'https://genius.com/Babyface-dont-take-it-so-personal-lyrics'

    def test_expected_values(self, lyrics):
        assert lyrics.id == self.id
        assert lyrics.lyrics == self.lyrics
        assert lyrics.full_lyrics == self.full_lyrics
        assert lyrics.has_rights == self.has_rights
        assert lyrics.text_language == self.text_language
        assert lyrics.show_translation == self.show_translation
        assert lyrics.url == self.url

    def test_de_json_none(self, client):
        assert Lyrics.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'id': self.id,
            'lyrics': self.lyrics,
            'full_lyrics': self.full_lyrics,
            'has_rights': self.has_rights,
            'show_translation': self.show_translation,
        }
        lyrics = Lyrics.de_json(json_dict, client)

        assert lyrics.id == self.id
        assert lyrics.lyrics == self.lyrics
        assert lyrics.full_lyrics == self.full_lyrics
        assert lyrics.has_rights == self.has_rights
        assert lyrics.show_translation == self.show_translation

    def test_de_json_all(self, client):
        json_dict = {
            'id': self.id,
            'lyrics': self.lyrics,
            'full_lyrics': self.full_lyrics,
            'has_rights': self.has_rights,
            'text_language': self.text_language,
            'show_translation': self.show_translation,
            'url': self.url,
        }
        lyrics = Lyrics.de_json(json_dict, client)

        assert lyrics.id == self.id
        assert lyrics.lyrics == self.lyrics
        assert lyrics.full_lyrics == self.full_lyrics
        assert lyrics.has_rights == self.has_rights
        assert lyrics.text_language == self.text_language
        assert lyrics.show_translation == self.show_translation
        assert lyrics.url == self.url

    def test_equality(self):
        a = Lyrics(self.id, self.lyrics, self.full_lyrics, self.has_rights, self.text_language, self.show_translation)
        b = Lyrics(self.id, self.lyrics, '', self.has_rights, self.text_language, False)
        c = Lyrics(10, self.lyrics, self.full_lyrics, self.has_rights, '', self.show_translation)
        d = Lyrics(self.id, self.lyrics, self.full_lyrics, self.has_rights, self.text_language, self.show_translation)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
