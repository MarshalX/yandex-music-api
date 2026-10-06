from typing import Dict

from yandex_music import Client, JSONType, PlayCounter


class TestPlayCounter:
    description = 'А&nbsp;вот и&nbsp;ответ на&nbsp;главный вопрос жизни, вселенной и&nbsp;всего такого'
    value = 42
    updated = True

    def test_expected_values(self, play_counter: PlayCounter) -> None:
        assert play_counter.value == self.value
        assert play_counter.description == self.description
        assert play_counter.updated == self.updated

    def test_de_json_none(self, client: Client) -> None:
        assert PlayCounter.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'value': self.value, 'description': self.description, 'updated': self.updated}
        play_counter = PlayCounter.de_json(json_dict, client)
        assert play_counter is not None

        assert play_counter.value == self.value
        assert play_counter.description == self.description
        assert play_counter.updated == self.updated

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'value': self.value, 'description': self.description, 'updated': self.updated}
        play_counter = PlayCounter.de_json(json_dict, client)
        assert play_counter is not None

        assert play_counter.value == self.value
        assert play_counter.description == self.description
        assert play_counter.updated == self.updated

    def test_equality(self) -> None:
        a = PlayCounter(self.value, self.description, self.updated)
        b = PlayCounter(30, self.description, self.updated)
        c = PlayCounter(self.value, self.description, False)
        d = PlayCounter(self.value, self.description, self.updated)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
