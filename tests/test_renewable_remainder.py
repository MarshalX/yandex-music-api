from typing import Dict

from yandex_music import Client, JSONType, RenewableRemainder


class TestRenewableRemainder:
    days = 0

    def test_expected_values(self, renewable_remainder: RenewableRemainder) -> None:
        assert renewable_remainder.days == self.days

    def test_de_json_none(self, client: Client) -> None:
        assert RenewableRemainder.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'days': self.days}
        renewable_remainder = RenewableRemainder.de_json(json_dict, client)
        assert renewable_remainder is not None

        assert renewable_remainder.days == self.days

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'days': self.days}
        renewable_remainder = RenewableRemainder.de_json(json_dict, client)
        assert renewable_remainder is not None

        assert renewable_remainder.days == self.days

    def test_equality(self) -> None:
        a = RenewableRemainder(self.days)
        b = RenewableRemainder(10)
        c = RenewableRemainder(self.days)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
