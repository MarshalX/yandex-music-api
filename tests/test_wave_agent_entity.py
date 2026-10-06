from typing import Dict

from yandex_music import Client, JSONType, WaveAgentEntity


class TestWaveAgentEntity:
    type = 'album'

    def test_expected_values(self, wave_agent_entity: WaveAgentEntity) -> None:
        assert wave_agent_entity.type == self.type

    def test_de_json_none(self, client: Client) -> None:
        assert WaveAgentEntity.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type}
        entity = WaveAgentEntity.de_json(json_dict, client)
        assert entity is not None

        assert entity.type == self.type

    def test_equality(self) -> None:
        a = WaveAgentEntity(type=self.type)
        b = WaveAgentEntity(type='artist')
        c = WaveAgentEntity(type=self.type)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
