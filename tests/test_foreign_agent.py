from yandex_music import ForeignAgent


class TestForeignAgent:
    reason = 'policy'
    title = 'ИСПОЛНИТЕЛЬ ПРИЗНАН ИНОАГЕНТОМ'

    def test_expected_value(self, foreign_agent):
        assert foreign_agent.reason == self.reason
        assert foreign_agent.title == self.title

    def test_de_json_none(self, client):
        assert ForeignAgent.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'reason': self.reason,
            'title': self.title,
        }
        foreign_agent = ForeignAgent.de_json(json_dict, client)

        assert foreign_agent.reason == self.reason
        assert foreign_agent.title == self.title

    def test_equality(self):
        a = ForeignAgent(reason=self.reason, title=self.title)
        b = ForeignAgent(reason='other', title=self.title)
        c = ForeignAgent(reason=self.reason, title=self.title)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
