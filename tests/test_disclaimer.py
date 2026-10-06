from typing import Dict

from yandex_music import Client, Disclaimer, ForeignAgent, JSONType


class TestDisclaimer:
    def test_expected_value(self, disclaimer: Disclaimer, foreign_agent: ForeignAgent) -> None:
        assert disclaimer.foreign_agent == foreign_agent

    def test_de_json_none(self, client: Client) -> None:
        assert Disclaimer.de_json({}, client) is None

    def test_de_json_all(self, client: Client, foreign_agent: ForeignAgent) -> None:
        json_dict: Dict[str, JSONType] = {
            'foreignAgent': foreign_agent.to_dict(),
        }
        disclaimer = Disclaimer.de_json(json_dict, client)
        assert disclaimer is not None

        assert disclaimer.foreign_agent == foreign_agent

    def test_equality(self, foreign_agent: ForeignAgent) -> None:
        a = Disclaimer(foreign_agent=foreign_agent)
        b = Disclaimer(foreign_agent=None)
        c = Disclaimer(foreign_agent=foreign_agent)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
