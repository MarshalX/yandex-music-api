from typing import Dict

from yandex_music import Client, JSONType, Stats


class TestStats:
    last_month_listeners = 15111
    last_month_listeners_delta = 5111

    def test_expected_values(self, stats: Stats) -> None:
        assert stats.last_month_listeners == stats.last_month_listeners
        assert stats.last_month_listeners_delta == stats.last_month_listeners_delta

    def test_de_json_none(self, client: Client) -> None:
        assert Stats.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'last_month_listeners': self.last_month_listeners,
            'last_month_listeners_delta': self.last_month_listeners_delta,
        }
        stats = Stats.de_json(json_dict, client)
        assert stats is not None

        assert stats.last_month_listeners == self.last_month_listeners
        assert stats.last_month_listeners_delta == self.last_month_listeners_delta

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'last_month_listeners': self.last_month_listeners,
            'last_month_listeners_delta': self.last_month_listeners_delta,
        }
        stats = Stats.de_json(json_dict, client)
        assert stats is not None

        assert stats.last_month_listeners == self.last_month_listeners
        assert stats.last_month_listeners_delta == self.last_month_listeners_delta

    def test_equality(self) -> None:
        a = Stats(self.last_month_listeners, self.last_month_listeners_delta)
        b = Stats(51234, self.last_month_listeners_delta)
        c = Stats(self.last_month_listeners, self.last_month_listeners_delta)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
