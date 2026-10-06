from typing import Dict

from yandex_music import Client, JSONType, NonAutoRenewable


class TestNonAutoRenewable:
    start = '2019-05-27T20:34:21+03:00'
    end = '2020-09-01T20:34:21+03:00'

    def test_expected_values(self, non_auto_renewable: NonAutoRenewable) -> None:
        assert non_auto_renewable.start == self.start
        assert non_auto_renewable.end == self.end

    def test_de_json_none(self, client: Client) -> None:
        assert NonAutoRenewable.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'start': self.start, 'end': self.end}
        non_auto_renewable = NonAutoRenewable.de_json(json_dict, client)
        assert non_auto_renewable is not None

        assert non_auto_renewable.start == self.start
        assert non_auto_renewable.end == self.end

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'start': self.start, 'end': self.end}
        non_auto_renewable = NonAutoRenewable.de_json(json_dict, client)
        assert non_auto_renewable is not None

        assert non_auto_renewable.start == self.start
        assert non_auto_renewable.end == self.end

    def test_equality(self) -> None:
        a = NonAutoRenewable(self.start, self.end)
        b = NonAutoRenewable('', self.end)
        c = NonAutoRenewable(self.start, self.end)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
