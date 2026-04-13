from yandex_music import CoverDerivedColors


class TestCoverDerivedColors:
    average = '#6d6e72'
    wave_text = '#e0e0e0'
    mini_player = '#b6b6b8'
    accent = '#97989a'

    def test_expected_values(self, cover_derived_colors):
        assert cover_derived_colors.average == self.average
        assert cover_derived_colors.wave_text == self.wave_text
        assert cover_derived_colors.mini_player == self.mini_player
        assert cover_derived_colors.accent == self.accent

    def test_de_json_none(self, client):
        assert CoverDerivedColors.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'average': self.average,
            'waveText': self.wave_text,
            'miniPlayer': self.mini_player,
            'accent': self.accent,
        }
        cover_derived_colors = CoverDerivedColors.de_json(json_dict, client)

        assert cover_derived_colors.average == self.average
        assert cover_derived_colors.wave_text == self.wave_text
        assert cover_derived_colors.mini_player == self.mini_player
        assert cover_derived_colors.accent == self.accent

    def test_equality(self):
        a = CoverDerivedColors(average=self.average, wave_text=self.wave_text)
        b = CoverDerivedColors(average='#000000', wave_text='#ffffff')
        c = CoverDerivedColors(average=self.average, wave_text=self.wave_text)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
