import pytest

from yandex_music import Landing


@pytest.fixture(scope='class')
def landing(blocks):
    return Landing(TestLanding.pumpkin, TestLanding.content_id, blocks)


class TestLanding:
    pumpkin = None
    content_id = None

    def test_expected_values(self, landing, blocks):
        assert landing.pumpkin == self.pumpkin
        assert landing.content_id == self.content_id
        assert landing.blocks == blocks

    def test_de_json_required(self, client, blocks):
        json_dict = {'pumpkin': self.pumpkin, 'content_id': self.content_id, 'blocks': blocks}
        landing = Landing.de_json(json_dict, client)

        assert landing.pumpkin == self.pumpkin
        assert landing.content_id == self.content_id
        assert landing.blocks == blocks

    def test_de_json_all(self, client, blocks):
        json_dict = {'pumpkin': self.pumpkin, 'content_id': self.content_id, 'blocks': blocks}
        landing = Landing.de_json(json_dict, client)

        assert landing.pumpkin == self.pumpkin
        assert landing.content_id == self.content_id
        assert landing.blocks == blocks

    def test_equality(self):
        pass
