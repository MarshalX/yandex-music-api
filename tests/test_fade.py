from typing import Dict

from yandex_music import Client, Fade, JSONType


class TestFade:
    in_start = 0.2
    in_stop = 1.5
    out_start = 191.9
    out_stop = 196.9

    def test_expected_values(self, fade: Fade) -> None:
        assert fade.in_start == self.in_start
        assert fade.in_stop == self.in_stop
        assert fade.out_start == self.out_start
        assert fade.out_stop == self.out_stop

    def test_de_json_none(self, client: Client) -> None:
        assert Fade.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'inStart': self.in_start,
            'inStop': self.in_stop,
            'outStart': self.out_start,
            'outStop': self.out_stop,
        }
        fade = Fade.de_json(json_dict, client)
        assert fade is not None

        assert fade.in_start == self.in_start
        assert fade.in_stop == self.in_stop
        assert fade.out_start == self.out_start
        assert fade.out_stop == self.out_stop

    def test_equality(self) -> None:
        a = Fade(in_start=self.in_start, in_stop=self.in_stop, out_start=self.out_start, out_stop=self.out_stop)
        b = Fade(in_start=0.0, in_stop=self.in_stop, out_start=self.out_start, out_stop=self.out_stop)
        c = Fade(in_start=self.in_start, in_stop=self.in_stop, out_start=self.out_start, out_stop=self.out_stop)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
