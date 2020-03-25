import pytest

from yandex_music import ShotEvent


@pytest.fixture(scope='class')
def shot_event(shot):
    return ShotEvent(TestShotType.event_id, [shot])


class TestShotType:
    event_id = '5e25fb2c0cf28e741cb996eb'

    def test_expected_values(self, shot_event, shot):
        assert shot_event.event_id == self.event_id
        assert shot_event.shots == [shot]

    def test_de_json_none(self, client):
        assert ShotEvent.de_json({}, client) is None

    def test_de_json_required(self, client, shot):
        json_dict = {'event_id': self.event_id, 'shots': [shot.to_dict()]}
        shot_event = ShotEvent.de_json(json_dict, client)

        assert shot_event.event_id == self.event_id
        assert shot_event.shots == [shot]

    def test_de_json_all(self, client, shot):
        json_dict = {'event_id': self.event_id, 'shots': [shot.to_dict()]}
        shot_event = ShotEvent.de_json(json_dict, client)

        assert shot_event.event_id == self.event_id
        assert shot_event.shots == [shot]

    def test_equality(self, shot):
        a = ShotEvent(self.event_id, [shot])
        b = ShotEvent('', [shot])
        c = ShotEvent(self.event_id, [])
        d = ShotEvent(self.event_id, [shot])

        assert a != b != c != d
        assert hash(a) != hash(b) != hash(c) != hash(d)
        assert a is not b is not c is not d

        assert a == d
        assert hash(a) == hash(d)
