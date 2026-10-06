from typing import Dict

from yandex_music import Client, Cover, JSONType, WaveAgent, WaveAgentEntity


class TestWaveAgent:
    animation_uri = 'https://example.com/animation'

    def test_expected_values(self, wave_agent: WaveAgent, cover: Cover, wave_agent_entity: WaveAgentEntity) -> None:
        assert wave_agent.animation_uri == self.animation_uri
        assert wave_agent.cover == cover
        assert wave_agent.entity == wave_agent_entity

    def test_de_json_none(self, client: Client) -> None:
        assert WaveAgent.de_json({}, client) is None

    def test_de_json_all(self, client: Client, cover: Cover, wave_agent_entity: WaveAgentEntity) -> None:
        json_dict: Dict[str, JSONType] = {
            'animationUri': self.animation_uri,
            'cover': cover.to_dict(),
            'entity': wave_agent_entity.to_dict(),
        }
        agent = WaveAgent.de_json(json_dict, client)
        assert agent is not None

        assert agent.animation_uri == self.animation_uri
        assert agent.cover == cover
        assert agent.entity == wave_agent_entity

    def test_equality(self, cover: Cover) -> None:
        a = WaveAgent(animation_uri=self.animation_uri, cover=cover)
        b = WaveAgent(animation_uri='https://other.com', cover=cover)
        c = WaveAgent(animation_uri=self.animation_uri, cover=cover)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
