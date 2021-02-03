from yandex_music import Description


class TestDescription:
    text = (
        'Американский певец и актёр, один из самых коммерчески успешных исполнителей популярной музыки XX века. '
        'Также известен как «король рок-н-ролла». Пресли популяризовал рок-н-ролл, хотя и не был первым '
        'исполнителем этого жанра. '
    )
    uri = 'http://ru.wikipedia.org/wiki/Пресли, Элвис'

    def test_expected_values(self, description):
        assert description.text == self.text
        assert description.uri == self.uri

    def test_de_json_none(self, client):
        assert Description.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'text': self.text, 'uri': self.uri}
        description = Description.de_json(json_dict, client)

        assert description.text == self.text
        assert description.uri == self.uri

    def test_de_json_all(self, client):
        json_dict = {'text': self.text, 'uri': self.uri}
        description = Description.de_json(json_dict, client)

        assert description.text == self.text
        assert description.uri == self.uri

    def test_equality(self):
        a = Description(self.text, self.uri)
        b = Description('', self.uri)
        c = Description(self.text, '')
        d = Description(self.text, self.uri)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
