from typing import Dict

from yandex_music import Client, ConcertDescription, JSONType


class TestConcertDescription:
    text = 'Захватывающее шоу для всех поклонников рок-музыки.'
    source = 'example.com'

    def test_expected_value(self, concert_description: ConcertDescription) -> None:
        assert concert_description.text == self.text
        assert concert_description.source == self.source

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertDescription.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'text': self.text,
            'source': self.source,
        }
        concert_description = ConcertDescription.de_json(json_dict, client)
        assert concert_description is not None

        assert concert_description.text == self.text
        assert concert_description.source == self.source

    def test_equality(self) -> None:
        a = ConcertDescription(text=self.text, source=self.source)
        b = ConcertDescription(text='Другой текст', source=self.source)
        c = ConcertDescription(text=self.text, source=self.source)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
