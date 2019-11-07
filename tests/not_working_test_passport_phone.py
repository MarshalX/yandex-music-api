import pytest

from yandex_music import PassportPhone


@pytest.fixture(scope='class')
def passport_phone():
    return PassportPhone(TestPassportPhone.phone)


class TestPassportPhone:
    phone = None

    def test_expected_values(self, passport_phone):
        assert passport_phone.phone == self.phone

    def test_de_json_required(self, client):
        json_dict = {'phone': self.phone}
        passport_phone = PassportPhone.de_json(json_dict, client)

        assert passport_phone.phone == self.phone

    def test_de_json_all(self, client):
        json_dict = {'phone': self.phone}
        passport_phone = PassportPhone.de_json(json_dict, client)

        assert passport_phone.phone == self.phone

    def test_equality(self):
        pass
