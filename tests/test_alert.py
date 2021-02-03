from yandex_music import Alert


class TestAlert:
    alert_id = 'xxx'
    text = 'тест Подписка скоро закончится. А вместе с ней закончатся музыка и подкасты без ограничений. Не надо так.'
    bg_color = '#FF5038'
    text_color = '#FFFFFF'
    alert_type = 'Churn_SubscriptionEnd_Music'
    close_button = False

    def test_expected_values(self, alert, alert_button):
        assert alert.alert_id == self.alert_id
        assert alert.text == self.text
        assert alert.bg_color == self.bg_color
        assert alert.text_color == self.text_color
        assert alert.alert_type == self.alert_type
        assert alert.button == alert_button
        assert alert.close_button == self.close_button

    def test_de_json_none(self, client):
        assert Alert.de_json({}, client) is None

    def test_de_json_required(self, client, alert_button):
        json_dict = {
            'alert_id': self.alert_id,
            'text': self.text,
            'bg_color': self.bg_color,
            'text_color': self.text_color,
            'alert_type': self.alert_type,
            'button': alert_button.to_dict(),
            'close_button': self.close_button,
        }
        alert = Alert.de_json(json_dict, client)

        assert alert.alert_id == self.alert_id
        assert alert.text == self.text
        assert alert.bg_color == self.bg_color
        assert alert.text_color == self.text_color
        assert alert.alert_type == self.alert_type
        assert alert.button == alert_button
        assert alert.close_button == self.close_button

    def test_de_json_all(self, client, alert_button):
        json_dict = {
            'alert_id': self.alert_id,
            'text': self.text,
            'bg_color': self.bg_color,
            'text_color': self.text_color,
            'alert_type': self.alert_type,
            'button': alert_button.to_dict(),
            'close_button': self.close_button,
        }
        alert = Alert.de_json(json_dict, client)

        assert alert.alert_id == self.alert_id
        assert alert.text == self.text
        assert alert.bg_color == self.bg_color
        assert alert.text_color == self.text_color
        assert alert.alert_type == self.alert_type
        assert alert.button == alert_button
        assert alert.close_button == self.close_button

    def test_equality(self, alert_button):
        a = Alert(
            self.alert_id, self.text, self.bg_color, self.text_color, self.alert_type, alert_button, self.close_button
        )
        b = Alert('', self.text, self.bg_color, self.text_color, self.alert_type, alert_button, self.close_button)
        c = Alert(
            self.alert_id, self.text, self.bg_color, self.text_color, self.alert_type, alert_button, self.close_button
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
