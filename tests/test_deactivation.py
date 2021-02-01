from yandex_music import Deactivation


class TestDeactivation:
    method = 'ussd'
    instructions = 'Отключение услуги: *301# (недоступно в роуминге)'

    def test_expected_values(self, deactivation):
        assert deactivation.method == self.method
        assert deactivation.instructions == self.instructions

    def test_de_json_none(self, client):
        assert Deactivation.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Deactivation.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'method': self.method}
        deactivation = Deactivation.de_json(json_dict, client)

        assert deactivation.method == self.method

    def test_de_json_all(self, client):
        json_dict = {'method': self.method, 'instructions': self.instructions}
        deactivation = Deactivation.de_json(json_dict, client)

        assert deactivation.method == self.method
        assert deactivation.instructions == self.instructions

    def test_equality(self):
        a = Deactivation(self.method, self.instructions)
        b = Deactivation('', self.instructions)
        c = Deactivation(self.method, self.instructions)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
