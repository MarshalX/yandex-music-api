import pytest

from yandex_music import LandingList


@pytest.fixture(scope='class')
def landing_list(playlist_id):
    return LandingList(
        TestLandingList.type,
        TestLandingList.type_for_from,
        TestLandingList.title,
        TestLandingList.id,
        TestLandingList.new_releases,
        [playlist_id],
        TestLandingList.podcasts,
    )


class TestLandingList:
    id = 'fNdCYuAs'
    title = 'Новые треки, альбомы и сборники'
    type = 'new-releases'
    type_for_from = 'new-releases'
    new_releases = [10704986, 10527291, 9479589]
    podcasts = [10532030, 8693523, 10509632]

    def test_expected_values(self, landing_list, playlist_id):
        assert landing_list.id == self.id
        assert landing_list.title == self.title
        assert landing_list.type == self.type
        assert landing_list.type_for_from == self.type_for_from
        assert landing_list.new_releases == self.new_releases
        assert landing_list.podcasts == self.podcasts
        assert landing_list.new_playlists == [playlist_id]

    def test_de_json_none(self, client):
        assert LandingList.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'title': self.title, 'type': self.type, 'type_for_from': self.type_for_from}
        landing_list = LandingList.de_json(json_dict, client)

        assert landing_list.title == self.title
        assert landing_list.type == self.type
        assert landing_list.type_for_from == self.type_for_from

    def test_de_json_all(self, client, playlist_id):
        json_dict = {
            'title': self.title,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'id': self.id,
            'new_releases': self.new_releases,
            'podcasts': self.podcasts,
            'new_playlists': [playlist_id.to_dict()],
        }
        landing_list = LandingList.de_json(json_dict, client)

        assert landing_list.id == self.id
        assert landing_list.title == self.title
        assert landing_list.type == self.type
        assert landing_list.type_for_from == self.type_for_from
        assert landing_list.new_releases == self.new_releases
        assert landing_list.podcasts == self.podcasts
        assert landing_list.new_playlists == [playlist_id]

    def test_equality(self, playlist_id):
        a = LandingList(self.type, self.type_for_from, self.title, self.id, self.new_releases, [playlist_id], [])
        b = LandingList(self.type, self.type_for_from, self.title, self.id, self.new_releases, [], [])
        c = LandingList(self.type, self.type_for_from, self.title, '', self.new_releases, [playlist_id], [])
        d = LandingList(self.type, self.type_for_from, self.title, self.id, self.new_releases, [playlist_id], [])

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
