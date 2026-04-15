from yandex_music import WaveAgentEntity


class TestWaveAgentEntity:
    type = 'album'

    def test_expected_values(self, wave_agent_entity):
        assert wave_agent_entity.type == self.type

    def test_de_json_none(self, client):
        assert WaveAgentEntity.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'type': self.type}
        entity = WaveAgentEntity.de_json(json_dict, client)

        assert entity.type == self.type

    def test_equality(self):
        a = WaveAgentEntity(type=self.type)
        b = WaveAgentEntity(type='artist')
        c = WaveAgentEntity(type=self.type)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
