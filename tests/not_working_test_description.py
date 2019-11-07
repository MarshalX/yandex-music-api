from yandex_music import Description


class TestDescription:
    text = None
    url = None

    def test_expected_values(self, description):
        assert description.text == self.text
        assert description.url == self.url

    def test_de_json_required(self, client):
        json_dict = {'text': self.text, 'url': self.url}
        description = Description.de_json(json_dict, client)

        assert description.text == self.text
        assert description.url == self.url

    def test_de_json_all(self, client):
        json_dict = {'text': self.text, 'url': self.url}
        description = Description.de_json(json_dict, client)

        assert description.text == self.text
        assert description.url == self.url

    def test_equality(self):
        pass
