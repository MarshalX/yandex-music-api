from typing import Dict

from yandex_music import Client, Icon, JSONType


class TestIcon:
    background_color = '#ff6665'
    image_url = 'avatars.yandex.net/get-music-misc/34161/rotor-genre-pop-icon/%%'

    def test_expected_values(self, icon: Icon) -> None:
        assert icon.background_color == self.background_color
        assert icon.image_url == self.image_url

    def test_de_json_none(self, client: Client) -> None:
        assert Icon.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'background_color': self.background_color, 'image_url': self.image_url}
        icon = Icon.de_json(json_dict, client)
        assert icon is not None

        assert icon.background_color == self.background_color
        assert icon.image_url == self.image_url

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'background_color': self.background_color, 'image_url': self.image_url}
        icon = Icon.de_json(json_dict, client)
        assert icon is not None

        assert icon.background_color == self.background_color
        assert icon.image_url == self.image_url

    def test_equality(self) -> None:
        a = Icon(self.background_color, self.image_url)
        b = Icon('#000000', self.image_url)
        c = Icon(self.background_color, '')
        d = Icon(self.background_color, self.image_url)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
