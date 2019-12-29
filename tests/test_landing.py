import pytest

from yandex_music import Landing


@pytest.fixture(scope='class')
def landing(block):
    return Landing(TestLanding.pumpkin, TestLanding.content_id, [block])


class TestLanding:
    pumpkin = False
    content_id = '-1159799446'

    def test_expected_values(self, landing, block):
        assert landing.pumpkin == self.pumpkin
        assert landing.content_id == self.content_id
        assert landing.blocks == [block]

    def test_de_json_none(self, client):
        assert Landing.de_json({}, client) is None

    def test_de_json_required(self, client, block):
        json_dict = {'pumpkin': self.pumpkin, 'content_id': self.content_id, 'blocks': [block.to_dict()]}
        landing = Landing.de_json(json_dict, client)

        assert landing.pumpkin == self.pumpkin
        assert landing.content_id == self.content_id
        assert landing.blocks == [block]

    def test_de_json_all(self, client, block):
        json_dict = {'pumpkin': self.pumpkin, 'content_id': self.content_id, 'blocks': [block.to_dict()]}
        landing = Landing.de_json(json_dict, client)

        assert landing.pumpkin == self.pumpkin
        assert landing.content_id == self.content_id
        assert landing.blocks == [block]

    def test_equality(self, block):
        a = Landing(self.pumpkin, self.content_id, [block])
        b = Landing(self.pumpkin, '', [block])
        c = Landing(self.pumpkin, self.content_id, [])
        d = Landing(self.pumpkin, self.content_id, [block])

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
