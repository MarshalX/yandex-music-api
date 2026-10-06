from typing import Dict

from yandex_music import Client, JSONType, Playlist, PlaylistsList


class TestPlaylistsList:
    def test_expected_value(self, playlists_list: PlaylistsList, playlist: Playlist) -> None:
        assert playlists_list.playlists == [playlist]

    def test_de_json_none(self, client: Client) -> None:
        assert PlaylistsList.de_json({}, client) is None

    def test_de_json_all(self, client: Client, playlist: Playlist) -> None:
        json_dict: Dict[str, JSONType] = {
            'playlists': [playlist.to_dict()],
        }
        playlists_list = PlaylistsList.de_json(json_dict, client)
        assert playlists_list is not None

        assert playlists_list.playlists == [playlist]

    def test_equality(self, playlist: Playlist) -> None:
        a = PlaylistsList(playlists=[playlist])
        b = PlaylistsList(playlists=None)
        c = PlaylistsList(playlists=[playlist])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
