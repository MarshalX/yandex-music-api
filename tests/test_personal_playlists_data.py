from yandex_music import PersonalPlaylistsData


class TestPersonalPlaylistsData:
    is_wizard_passed = True

    def test_expected_values(self, personal_playlists_data):
        assert personal_playlists_data.is_wizard_passed == self.is_wizard_passed

    def test_de_json_none(self, client):
        assert PersonalPlaylistsData.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'is_wizard_passed': self.is_wizard_passed}
        personal_playlists_data = PersonalPlaylistsData.de_json(json_dict, client)

        assert personal_playlists_data.is_wizard_passed == self.is_wizard_passed

    def test_de_json_all(self, client):
        json_dict = {'is_wizard_passed': self.is_wizard_passed}
        personal_playlists_data = PersonalPlaylistsData.de_json(json_dict, client)

        assert personal_playlists_data.is_wizard_passed == self.is_wizard_passed

    def test_equality(self):
        a = PersonalPlaylistsData(self.is_wizard_passed)
        b = PersonalPlaylistsData(False)
        c = PersonalPlaylistsData(self.is_wizard_passed)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
