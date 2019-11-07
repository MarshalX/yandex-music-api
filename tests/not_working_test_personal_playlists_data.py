import pytest

from yandex_music import PersonalPlaylistsData


@pytest.fixture(scope='class')
def personal_playlists_data():
    return PersonalPlaylistsData(TestPersonalPlaylistsData.is_wizard_passed)


class TestPersonalPlaylistsData:
    is_wizard_passed = None

    def test_expected_values(self, personal_playlists_data):
        assert personal_playlists_data.is_wizard_passed == self.is_wizard_passed

    def test_de_json_required(self, client):
        json_dict = {'is_wizard_passed': self.is_wizard_passed}
        personal_playlists_data = PersonalPlaylistsData.de_json(json_dict, client)

        assert personal_playlists_data.is_wizard_passed == self.is_wizard_passed

    def test_de_json_all(self, client):
        json_dict = {'is_wizard_passed': self.is_wizard_passed}
        personal_playlists_data = PersonalPlaylistsData.de_json(json_dict, client)

        assert personal_playlists_data.is_wizard_passed == self.is_wizard_passed

    def test_equality(self):
        pass
