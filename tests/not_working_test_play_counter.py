from yandex_music import PlayCounter


class TestPlayCounter:
    value = None
    updated = None

    def test_expected_values(self, play_counter, description):
        assert play_counter.value == self.value
        assert play_counter.description == description
        assert play_counter.updated == self.updated

    def test_de_json_required(self, client, description):
        json_dict = {'value': self.value, 'description': description, 'updated': self.updated}
        play_counter = PlayCounter.de_json(json_dict, client)

        assert play_counter.value == self.value
        assert play_counter.description == description
        assert play_counter.updated == self.updated

    def test_de_json_all(self, client, description):
        json_dict = {'value': self.value, 'description': description, 'updated': self.updated}
        play_counter = PlayCounter.de_json(json_dict, client)

        assert play_counter.value == self.value
        assert play_counter.description == description
        assert play_counter.updated == self.updated

    def test_equality(self):
        pass
