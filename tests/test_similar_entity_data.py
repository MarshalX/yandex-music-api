from yandex_music import SimilarEntityData


class TestSimilarEntityData:
    def test_expected_values(self, similar_entity_data, wave, wave_agent):
        assert similar_entity_data.wave == wave
        assert similar_entity_data.agent == wave_agent

    def test_de_json_none(self, client):
        assert SimilarEntityData.de_json({}, client) is None

    def test_de_json_all(self, client, wave, wave_agent):
        json_dict = {
            'wave': wave.to_dict(),
            'agent': wave_agent.to_dict(),
        }
        data = SimilarEntityData.de_json(json_dict, client)

        assert data.wave == wave
        assert data.agent == wave_agent

    def test_equality(self, wave, wave_agent):
        a = SimilarEntityData(wave=wave, agent=wave_agent)
        b = SimilarEntityData(wave=None, agent=wave_agent)
        c = SimilarEntityData(wave=wave, agent=wave_agent)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
