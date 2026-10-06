from typing import Dict

from yandex_music import Client, JSONType, LicenceTextPart


class TestLicenceTextPart:
    text = 'Условия подписки.'
    url = 'https://yandex.ru/legal/yandex_plus_conditions/'

    def test_expected_values(self, licence_text_part: LicenceTextPart) -> None:
        assert licence_text_part.text == self.text
        assert licence_text_part.url == self.url

    def test_de_json_none(self, client: Client) -> None:
        assert LicenceTextPart.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert LicenceTextPart.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'text': self.text}
        licence_text_part = LicenceTextPart.de_json(json_dict, client)
        assert licence_text_part is not None

        assert licence_text_part.text == self.text

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'text': self.text, 'url': self.url}
        licence_text_part = LicenceTextPart.de_json(json_dict, client)
        assert licence_text_part is not None

        assert licence_text_part.text == self.text
        assert licence_text_part.url == self.url

    def test_equality(self) -> None:
        a = LicenceTextPart(self.text, self.url)
        b = LicenceTextPart('', self.url)
        c = LicenceTextPart(self.text, self.url)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
