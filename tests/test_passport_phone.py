from typing import Dict

from yandex_music import Client, JSONType, PassportPhone


class TestPassportPhone:
    phone = '+375295773423'

    def test_expected_values(self, passport_phone: PassportPhone) -> None:
        assert passport_phone.phone == self.phone

    def test_de_json_none(self, client: Client) -> None:
        assert PassportPhone.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert PassportPhone.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'phone': self.phone}
        passport_phone = PassportPhone.de_json(json_dict, client)
        assert passport_phone is not None

        assert passport_phone.phone == self.phone

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'phone': self.phone}
        passport_phone = PassportPhone.de_json(json_dict, client)
        assert passport_phone is not None

        assert passport_phone.phone == self.phone

    def test_equality(self) -> None:
        a = PassportPhone(self.phone)
        b = PassportPhone('')
        c = PassportPhone(self.phone)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
