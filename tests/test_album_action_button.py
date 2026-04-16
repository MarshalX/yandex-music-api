from yandex_music import AlbumActionButton


class TestAlbumActionButton:
    text = 'Рецензии «Риса за Творчество»'
    url = 'yandexmusic://cards/promo/rzt_quok2'
    color = '#27272A'

    def test_expected_values(self, album_action_button):
        assert album_action_button.text == self.text
        assert album_action_button.url == self.url
        assert album_action_button.color == self.color

    def test_de_json_none(self, client):
        assert AlbumActionButton.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {}
        assert AlbumActionButton.de_json(json_dict, client) is None

    def test_de_json_all(self, client):
        json_dict = {'text': self.text, 'url': self.url, 'color': self.color}
        album_action_button = AlbumActionButton.de_json(json_dict, client)

        assert album_action_button.text == self.text
        assert album_action_button.url == self.url
        assert album_action_button.color == self.color

    def test_equality(self):
        a = AlbumActionButton(self.text, self.url, self.color)
        b = AlbumActionButton('Другой текст', self.url, self.color)
        c = AlbumActionButton(self.text, '', self.color)
        d = AlbumActionButton(self.text, self.url, self.color)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
