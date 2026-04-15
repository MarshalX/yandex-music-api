from yandex_music import Presaves


class TestPresaves:
    def test_expected_value(self, presaves, album):
        assert presaves.upcoming_albums == [album]
        assert presaves.released_albums == [album]

    def test_de_json_none(self, client):
        assert Presaves.de_json({}, client) is None

    def test_de_json_all(self, client, album):
        json_dict = {
            'upcomingAlbums': [album.to_dict()],
            'releasedAlbums': [album.to_dict()],
        }
        presaves = Presaves.de_json(json_dict, client)

        assert presaves.upcoming_albums == [album]
        assert presaves.released_albums == [album]

    def test_equality(self, album):
        a = Presaves(upcoming_albums=[album], released_albums=[album])
        b = Presaves(upcoming_albums=None, released_albums=None)
        c = Presaves(upcoming_albums=[album], released_albums=[album])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
