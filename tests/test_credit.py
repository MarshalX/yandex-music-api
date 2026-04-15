from yandex_music import Credit


class TestCredit:
    title = 'Автор музыки'
    value = 'Тестовый Исполнитель'

    def test_expected_value(self, credit):
        assert credit.title == self.title
        assert credit.value == self.value

    def test_de_json_none(self, client):
        assert Credit.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'value': self.value,
        }
        credit = Credit.de_json(json_dict, client)

        assert credit.title == self.title
        assert credit.value == self.value

    def test_equality(self):
        a = Credit(title=self.title, value=self.value)
        b = Credit(title='Лейбл', value=self.value)
        c = Credit(title=self.title, value=self.value)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
