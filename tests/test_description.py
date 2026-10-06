from typing import Dict

from yandex_music import Client, Description, JSONType


class TestDescription:
    text = (
        'Американский певец и актёр, один из самых коммерчески успешных исполнителей популярной музыки XX века. '
        'Также известен как «король рок-н-ролла». Пресли популяризовал рок-н-ролл, хотя и не был первым '
        'исполнителем этого жанра. '
    )
    uri = 'http://ru.wikipedia.org/wiki/Пресли, Элвис'

    def test_expected_values(self, description: Description) -> None:
        assert description.text == self.text
        assert description.uri == self.uri

    def test_de_json_none(self, client: Client) -> None:
        assert Description.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'text': self.text}
        description = Description.de_json(json_dict, client)
        assert description is not None

        assert description.text == self.text

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'text': self.text, 'uri': self.uri}
        description = Description.de_json(json_dict, client)
        assert description is not None

        assert description.text == self.text
        assert description.uri == self.uri

    def test_equality(self) -> None:
        a = Description(self.text, self.uri)
        b = Description('', self.uri)
        c = Description(self.text, '')
        d = Description(self.text, self.uri)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
