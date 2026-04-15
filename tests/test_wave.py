from yandex_music import Wave


class TestWave:
    name = 'Test Wave'
    description = 'Моя волна по альбому'
    seeds = ['album:12345']

    def test_expected_values(self, wave):
        assert wave.name == self.name
        assert wave.description == self.description
        assert wave.seeds == self.seeds

    def test_de_json_none(self, client):
        assert Wave.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'name': self.name,
            'description': self.description,
            'seeds': self.seeds,
        }
        wave = Wave.de_json(json_dict, client)

        assert wave.name == self.name
        assert wave.description == self.description
        assert wave.seeds == self.seeds

    def test_equality(self):
        a = Wave(name=self.name, seeds=self.seeds)
        b = Wave(name='Other', seeds=['artist:999'])
        c = Wave(name=self.name, seeds=self.seeds)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
