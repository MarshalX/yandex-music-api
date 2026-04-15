from yandex_music import Disclaimer


class TestDisclaimer:
    def test_expected_value(self, disclaimer, foreign_agent):
        assert disclaimer.foreign_agent == foreign_agent

    def test_de_json_none(self, client):
        assert Disclaimer.de_json({}, client) is None

    def test_de_json_all(self, client, foreign_agent):
        json_dict = {
            'foreignAgent': foreign_agent.to_dict(),
        }
        disclaimer = Disclaimer.de_json(json_dict, client)

        assert disclaimer.foreign_agent == foreign_agent

    def test_equality(self, foreign_agent):
        a = Disclaimer(foreign_agent=foreign_agent)
        b = Disclaimer(foreign_agent=None)
        c = Disclaimer(foreign_agent=foreign_agent)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
