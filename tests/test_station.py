from yandex_music import Station


class TestStation:
    name = 'На вашей волне'
    id_for_from = 'user-561231028'
    full_image_url = 'avatars.yandex.net/get-music-misc/30221/rotor-activity-sex-full-image-3sv6j/%%'
    mts_full_image_url = 'avatars.yandex.net/get-music-misc/2413828/rotor-activity-sex-mts-full-image-sYtDD/%%'
    special_context = False
    listeners = 100500
    login = 'fake-login'
    full_name = 'Fake Name'
    display_name = 'fake-display-name'
    visibility = 'public'

    def test_expected_values(self, station, id_, icon, restrictions):
        assert station.id == id_
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == icon
        assert station.geocell_icon == icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions
        assert station.full_image_url == self.full_image_url
        assert station.mts_full_image_url == self.mts_full_image_url
        assert station.parent_id == id_
        assert station.special_context == self.special_context
        assert station.listeners == self.listeners
        assert station.login == self.login
        assert station.full_name == self.full_name
        assert station.display_name == self.display_name
        assert station.visibility == self.visibility

    def test_de_json_none(self, client):
        assert Station.de_json({}, client) is None

    def test_de_json_required(self, client, id_, icon, restrictions):
        json_dict = {
            'id': id_.to_dict(),
            'name': self.name,
            'icon': icon.to_dict(),
            'mts_icon': icon.to_dict(),
            'geocell_icon': icon.to_dict(),
            'id_for_from': self.id_for_from,
            'restrictions': restrictions.to_dict(),
            'restrictions2': restrictions.to_dict(),
        }
        station = Station.de_json(json_dict, client)

        assert station.id == id_
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == icon
        assert station.geocell_icon == icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions

    def test_de_json_all(self, client, id_, icon, restrictions):
        json_dict = {
            'id': id_.to_dict(),
            'name': self.name,
            'icon': icon.to_dict(),
            'mts_icon': icon.to_dict(),
            'geocell_icon': icon.to_dict(),
            'id_for_from': self.id_for_from,
            'restrictions': restrictions.to_dict(),
            'restrictions2': restrictions.to_dict(),
            'parent_id': id_.to_dict(),
            'full_image_url': self.full_image_url,
            'mts_full_image_url': self.mts_full_image_url,
            'specialContext': self.special_context,
            'listeners': self.listeners,
            'login': self.login,
            'fullName': self.full_name,
            'displayName': self.display_name,
            'visibility': self.visibility,
        }
        station = Station.de_json(json_dict, client)

        assert station.id == id_
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == icon
        assert station.geocell_icon == icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions
        assert station.full_image_url == self.full_image_url
        assert station.mts_full_image_url == self.mts_full_image_url
        assert station.parent_id == id_
        assert station.special_context == self.special_context
        assert station.listeners == self.listeners
        assert station.login == self.login
        assert station.full_name == self.full_name
        assert station.display_name == self.display_name
        assert station.visibility == self.visibility

    def test_de_json_without_geocell_icon(self, client, id_, icon, restrictions):
        json_dict = {
            'id': id_.to_dict(),
            'name': self.name,
            'icon': icon.to_dict(),
            'mtsIcon': icon.to_dict(),
            'idForFrom': self.id_for_from,
            'restrictions': restrictions.to_dict(),
            'restrictions2': restrictions.to_dict(),
            'specialContext': self.special_context,
        }
        station = Station.de_json(json_dict, client)

        assert station.geocell_icon is None
        assert station.special_context == self.special_context

    def test_equality(self, id_, icon, restrictions):
        a = Station(id_, self.name, icon, icon, icon, self.id_for_from, restrictions, restrictions)
        b = Station(id_, self.name, None, icon, icon, self.id_for_from, restrictions, restrictions)
        c = Station(id_, '', icon, icon, icon, self.id_for_from, restrictions, restrictions)
        d = Station(id_, self.name, icon, icon, icon, self.id_for_from, restrictions, restrictions)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
