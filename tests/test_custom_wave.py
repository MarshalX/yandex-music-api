from typing import Dict

from yandex_music import Client, CustomWave, JSONType


class TestCustomWave:
    title = 'В стиле: Трибунал'
    animation_url = 'https://music-custom-wave-media.s3.yandex.net/base.json'
    position = 'default'
    header = 'Моя волна по плейлисту'
    background_image_url = (
        'avatars.mds.yandex.net/get-music-misc/28052/custom-wave-default-playlist-background.image/%%'
    )

    def test_expected_values(self, custom_wave: CustomWave) -> None:
        assert custom_wave.title == self.title
        assert custom_wave.animation_url == self.animation_url
        assert custom_wave.position == self.position

    def test_de_json_none(self, client: Client) -> None:
        assert CustomWave.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'animation_url': self.animation_url,
            'position': self.position,
        }
        customwave = CustomWave.de_json(json_dict, client)
        assert customwave is not None

        assert customwave.title == self.title
        assert customwave.animation_url == self.animation_url
        assert customwave.position == self.position

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'animation_url': self.animation_url,
            'position': self.position,
            'header': self.header,
            'backgroundImageUrl': self.background_image_url,
        }
        customwave = CustomWave.de_json(json_dict, client)
        assert customwave is not None

        assert customwave.title == self.title
        assert customwave.animation_url == self.animation_url
        assert customwave.position == self.position
        assert customwave.header == self.header
        assert customwave.background_image_url == self.background_image_url

    def test_equality(self) -> None:
        a = CustomWave(self.title, self.animation_url, self.position)
        b = CustomWave('', self.animation_url, self.position)
        c = CustomWave(self.title, self.animation_url, self.position)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
