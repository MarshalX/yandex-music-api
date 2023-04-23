import pytest

from yandex_music import CustomWave


class TestCustomWave:
    title = 'В стиле: Трибунал'
    animation_url = 'https://music-custom-wave-media.s3.yandex.net/base.json'
    position = 'default'

    def test_expected_values(self, custom_wave):
        assert custom_wave.title == self.title
        assert custom_wave.animation_url == self.animation_url
        assert custom_wave.position == self.position

    def test_de_json_none(self, client):
        assert CustomWave.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'title': self.title,
            'animation_url': self.animation_url,
            'position': self.position,
        }
        customwave = CustomWave.de_json(json_dict, client)

        assert customwave.title == self.title
        assert customwave.animation_url == self.animation_url
        assert customwave.position == self.position

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'animation_url': self.animation_url,
            'position': self.position,
        }
        customwave = CustomWave.de_json(json_dict, client)

        assert customwave.title == self.title
        assert customwave.animation_url == self.animation_url
        assert customwave.position == self.position

    def test_equality(self):
        a = CustomWave(self.title, self.animation_url, self.position)
        b = CustomWave('', self.animation_url, self.position)
        c = CustomWave(self.title, self.animation_url, self.position)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
