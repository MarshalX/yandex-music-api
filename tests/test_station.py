from yandex_music import Station


class TestStation:
    name = 'На вашей волне'
    id_for_from = 'user-561231028'

    def test_expected_values(self, station, id, icon, restrictions):
        assert station.id == id
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == icon
        assert station.geocell_icon == icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions
        assert station.parent_id == id

    def test_de_json_required(self, client, id, icon, restrictions):
        json_dict = {'id': id.to_dict(), 'name': self.name, 'icon': icon.to_dict(), 'mts_icon': icon.to_dict(),
                     'geocell_icon': icon.to_dict(), 'id_for_from': self.id_for_from,
                     'restrictions': restrictions.to_dict(), 'restrictions2': restrictions.to_dict()}
        station = Station.de_json(json_dict, client)

        assert station.id == id
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == icon
        assert station.geocell_icon == icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions

    def test_de_json_all(self, client, id, icon, restrictions):
        json_dict = {'id': id.to_dict(), 'name': self.name, 'icon': icon.to_dict(), 'mts_icon': icon.to_dict(),
                     'geocell_icon': icon.to_dict(), 'id_for_from': self.id_for_from,
                     'restrictions': restrictions.to_dict(), 'restrictions2': restrictions.to_dict(),
                     'parent_id': id.to_dict()}
        station = Station.de_json(json_dict, client)

        assert station.id == id
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == icon
        assert station.geocell_icon == icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions
        assert station.parent_id == id

    def test_equality(self, id, icon, restrictions):
        a = Station(id, icon, self.name, icon, icon, icon, self.id_for_from, restrictions, restrictions)
        b = Station(id, icon, self.name, None, icon, icon, self.id_for_from, restrictions, restrictions)
        c = Station(id, icon, '', icon, icon, None, self.id_for_from, restrictions, restrictions)
        d = Station(id, icon, self.name, icon, icon, icon, self.id_for_from, restrictions, restrictions)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
