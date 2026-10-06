from typing import Dict, List

from yandex_music import Client, GeneratedPlaylist, JSONType, Playlist


class TestGeneratedPlaylist:
    type = 'playlistOfTheDay'
    ready = True
    notify = False
    description: List[JSONType] = []
    preview_description = 'Звучит по-вашему каждый день'

    def test_expected_values(self, generated_playlist: GeneratedPlaylist, playlist: Playlist) -> None:
        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == playlist
        assert generated_playlist.description == self.description
        assert generated_playlist.preview_description == self.preview_description

    def test_de_json_none(self, client: Client) -> None:
        assert GeneratedPlaylist.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert GeneratedPlaylist.de_list([], client) == []

    def test_de_json_required(self, client: Client, playlist: Playlist) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'ready': self.ready,
            'notify': self.notify,
            'data': playlist.to_dict(),
        }
        generated_playlist = GeneratedPlaylist.de_json(json_dict, client)
        assert generated_playlist is not None

        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == playlist

    def test_de_json_all(self, client: Client, playlist: Playlist) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'ready': self.ready,
            'notify': self.notify,
            'data': playlist.to_dict(),
            'description': self.description,
            'preview_description': self.preview_description,
        }
        generated_playlist = GeneratedPlaylist.de_json(json_dict, client)
        assert generated_playlist is not None

        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == playlist
        assert generated_playlist.description == self.description
        assert generated_playlist.preview_description == self.preview_description

    def test_equality(self, playlist: Playlist) -> None:
        a = GeneratedPlaylist(self.type, self.ready, self.notify, playlist)
        b = GeneratedPlaylist(self.type, False, self.notify, None)
        c = GeneratedPlaylist(self.type, self.ready, self.notify, playlist)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
