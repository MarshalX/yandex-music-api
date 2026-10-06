from typing import Dict

from yandex_music import AlertButton, Client, JSONType


class TestAlertButton:
    text = 'Оформить подписку'
    bg_color = '#FFFFFF'
    text_color = '#191919'
    uri = 'https://plus.yandex.ru/?source=music_web_churn_subscriptionend'

    def test_expected_values(self, alert_button: AlertButton) -> None:
        assert alert_button.text == self.text
        assert alert_button.bg_color == self.bg_color
        assert alert_button.text_color == self.text_color
        assert alert_button.uri == self.uri

    def test_de_json_none(self, client: Client) -> None:
        assert AlertButton.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'text': self.text,
            'bg_color': self.bg_color,
            'text_color': self.text_color,
            'uri': self.uri,
        }
        alert_button = AlertButton.de_json(json_dict, client)
        assert alert_button is not None

        assert alert_button.text == self.text
        assert alert_button.bg_color == self.bg_color
        assert alert_button.text_color == self.text_color
        assert alert_button.uri == self.uri

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'text': self.text,
            'bg_color': self.bg_color,
            'text_color': self.text_color,
            'uri': self.uri,
        }
        alert_button = AlertButton.de_json(json_dict, client)
        assert alert_button is not None

        assert alert_button.text == self.text
        assert alert_button.bg_color == self.bg_color
        assert alert_button.text_color == self.text_color
        assert alert_button.uri == self.uri

    def test_equality(self) -> None:
        a = AlertButton(self.text, self.bg_color, self.text_color, self.uri)
        b = AlertButton('', self.bg_color, self.text_color, '')
        c = AlertButton(self.text, self.bg_color, self.text_color, self.uri)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
