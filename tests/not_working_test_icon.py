from yandex_music import Icon


class TestIcon:
    background_color = None
    image_url = None

    def test_expected_values(self, icon):
        assert icon.background_color == self.background_color
        assert icon.image_url == self.image_url

    def test_de_json_required(self, client):
        json_dict = {'background_color': self.background_color, 'image_url': self.image_url}
        icon = Icon.de_json(json_dict, client)

        assert icon.background_color == self.background_color
        assert icon.image_url == self.image_url

    def test_de_json_all(self, client):
        json_dict = {'background_color': self.background_color, 'image_url': self.image_url}
        icon = Icon.de_json(json_dict, client)

        assert icon.background_color == self.background_color
        assert icon.image_url == self.image_url

    def test_equality(self):
        pass
