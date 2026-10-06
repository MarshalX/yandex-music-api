from typing import Dict

from yandex_music import Client, Credit, Credits, JSONType


class TestCredits:
    def test_expected_value(self, credits_: Credits, credit: Credit) -> None:
        assert credits_.credits == [credit]

    def test_de_json_none(self, client: Client) -> None:
        assert Credits.de_json({}, client) is None

    def test_de_json_all(self, client: Client, credit: Credit) -> None:
        json_dict: Dict[str, JSONType] = {
            'credits': [credit.to_dict()],
        }
        credits_ = Credits.de_json(json_dict, client)
        assert credits_ is not None

        assert credits_.credits == [credit]

    def test_equality(self, credit: Credit) -> None:
        a = Credits(credits=[credit])
        b = Credits(credits=None)
        c = Credits(credits=[credit])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
