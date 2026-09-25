from yandex_music import WaveSettingsBlock


class TestWaveSettingsBlock:
    type = 'contexts'

    def test_expected_values(self, wave_settings_block, station):
        assert wave_settings_block.type == self.type
        assert wave_settings_block.items == [station]

    def test_de_json_none(self, client):
        assert WaveSettingsBlock.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert WaveSettingsBlock.de_list([], client) == []

    def test_de_json_all(self, client, station):
        json_dict = {'type': self.type, 'items': [station.to_dict()]}
        wave_settings_block = WaveSettingsBlock.de_json(json_dict, client)

        assert wave_settings_block.type == self.type
        assert wave_settings_block.items == [station]

    def test_equality(self, station):
        a = WaveSettingsBlock(self.type, [station])
        b = WaveSettingsBlock('other', [station])
        c = WaveSettingsBlock(self.type, [station])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
