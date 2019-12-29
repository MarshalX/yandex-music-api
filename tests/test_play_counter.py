from yandex_music import PlayCounter


class TestPlayCounter:
    description = 'А&nbsp;вот и&nbsp;ответ на&nbsp;главный вопрос жизни, вселенной и&nbsp;всего такого'
    value = 42
    updated = True

    def test_expected_values(self, play_counter):
        assert play_counter.value == self.value
        assert play_counter.description == self.description
        assert play_counter.updated == self.updated

    def test_de_json_none(self, client):
        assert PlayCounter.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'value': self.value, 'description': self.description, 'updated': self.updated}
        play_counter = PlayCounter.de_json(json_dict, client)

        assert play_counter.value == self.value
        assert play_counter.description == self.description
        assert play_counter.updated == self.updated

    def test_de_json_all(self, client):
        json_dict = {'value': self.value, 'description': self.description, 'updated': self.updated}
        play_counter = PlayCounter.de_json(json_dict, client)

        assert play_counter.value == self.value
        assert play_counter.description == self.description
        assert play_counter.updated == self.updated

    def test_equality(self):
        a = PlayCounter(self.value, self.description, self.updated)
        b = PlayCounter(30, self.description, self.updated)
        c = PlayCounter(self.value, self.description, False)
        d = PlayCounter(self.value, self.description, self.updated)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
