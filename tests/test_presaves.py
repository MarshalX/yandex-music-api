from typing import Dict

from yandex_music import Album, Client, JSONType, Presaves


class TestPresaves:
    def test_expected_value(self, presaves: Presaves, album: Album) -> None:
        assert presaves.upcoming_albums == [album]
        assert presaves.released_albums == [album]

    def test_de_json_none(self, client: Client) -> None:
        assert Presaves.de_json({}, client) is None

    def test_de_json_all(self, client: Client, album: Album) -> None:
        json_dict: Dict[str, JSONType] = {
            'upcomingAlbums': [album.to_dict()],
            'releasedAlbums': [album.to_dict()],
        }
        presaves = Presaves.de_json(json_dict, client)
        assert presaves is not None

        assert presaves.upcoming_albums == [album]
        assert presaves.released_albums == [album]

    def test_equality(self, album: Album) -> None:
        a = Presaves(upcoming_albums=[album], released_albums=[album])
        b = Presaves(upcoming_albums=None, released_albums=None)
        c = Presaves(upcoming_albums=[album], released_albums=[album])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
