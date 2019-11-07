import pytest

from yandex_music import Label


@pytest.fixture(scope='class')
def label():
    return Label(TestLabel.id, TestLabel.name)


class TestLabel:
    name = None

    def test_expected_values(self, label, id):
        assert label.id == id
        assert label.name == self.name

    def test_de_json_required(self, client, id):
        json_dict = {'id': id, 'name': self.name}
        label = Label.de_json(json_dict, client)

        assert label.id == id
        assert label.name == self.name

    def test_de_json_all(self, client, id):
        json_dict = {'id': id, 'name': self.name}
        label = Label.de_json(json_dict, client)

        assert label.id == id
        assert label.name == self.name

    def test_equality(self):
        pass
