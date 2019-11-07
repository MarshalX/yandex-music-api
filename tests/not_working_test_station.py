from yandex_music import Station


class TestStation:
    name = None
    id_for_from = None

    def test_expected_values(self, station, id, icon, mts_icon, geocell_icon, restrictions, restrictions2, parent_id):
        assert station.id == id
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == mts_icon
        assert station.geocell_icon == geocell_icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions2
        assert station.parent_id == parent_id

    def test_de_json_required(self, client, id, icon, mts_icon, geocell_icon, restrictions, restrictions2):
        json_dict = {'id': id, 'name': self.name, 'icon': icon, 'mts_icon': mts_icon, 'geocell_icon': geocell_icon,
                     'id_for_from': self.id_for_from, 'restrictions': restrictions, 'restrictions2': restrictions2}
        station = Station.de_json(json_dict, client)

        assert station.id == id
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == mts_icon
        assert station.geocell_icon == geocell_icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions2

    def test_de_json_all(self, client, id, icon, mts_icon, geocell_icon, restrictions, restrictions2, parent_id):
        json_dict = {'id': id, 'name': self.name, 'icon': icon, 'mts_icon': mts_icon, 'geocell_icon': geocell_icon,
                     'id_for_from': self.id_for_from, 'restrictions': restrictions, 'restrictions2': restrictions2,
                     'parent_id': parent_id}
        station = Station.de_json(json_dict, client)

        assert station.id == id
        assert station.name == self.name
        assert station.icon == icon
        assert station.mts_icon == mts_icon
        assert station.geocell_icon == geocell_icon
        assert station.id_for_from == self.id_for_from
        assert station.restrictions == restrictions
        assert station.restrictions2 == restrictions2
        assert station.parent_id == parent_id

    def test_equality(self):
        pass
