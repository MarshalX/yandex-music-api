from typing import Dict

from yandex_music import AlbumActionButton, Client, JSONType


class TestAlbumActionButton:
    text = 'Рецензии «Риса за Творчество»'
    url = 'yandexmusic://cards/promo/rzt_quok2'
    color = '#27272A'

    def test_expected_values(self, album_action_button: AlbumActionButton) -> None:
        assert album_action_button.text == self.text
        assert album_action_button.url == self.url
        assert album_action_button.color == self.color

    def test_de_json_none(self, client: Client) -> None:
        assert AlbumActionButton.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {}
        assert AlbumActionButton.de_json(json_dict, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'text': self.text, 'url': self.url, 'color': self.color}
        album_action_button = AlbumActionButton.de_json(json_dict, client)
        assert album_action_button is not None

        assert album_action_button.text == self.text
        assert album_action_button.url == self.url
        assert album_action_button.color == self.color

    def test_equality(self) -> None:
        a = AlbumActionButton(self.text, self.url, self.color)
        b = AlbumActionButton('Другой текст', self.url, self.color)
        c = AlbumActionButton(self.text, '', self.color)
        d = AlbumActionButton(self.text, self.url, self.color)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
