from yandex_music import GeneratedPlaylist


class TestGeneratedPlaylist:
    type = 'playlistOfTheDay'
    ready = True
    notify = False
    description = []

    def test_expected_values(self, generated_playlist, playlist):
        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == playlist
        assert generated_playlist.description == self.description

    def test_de_json_none(self, client):
        assert GeneratedPlaylist.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert GeneratedPlaylist.de_list({}, client) == []

    def test_de_json_required(self, client, playlist):
        json_dict = {'type': self.type, 'ready': self.ready, 'notify': self.notify, 'data': playlist.to_dict()}
        generated_playlist = GeneratedPlaylist.de_json(json_dict, client)

        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == playlist

    def test_de_json_all(self, client, playlist):
        json_dict = {
            'type': self.type,
            'ready': self.ready,
            'notify': self.notify,
            'data': playlist.to_dict(),
            'description': self.description,
        }
        generated_playlist = GeneratedPlaylist.de_json(json_dict, client)

        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == playlist
        assert generated_playlist.description == self.description

    def test_equality(self, playlist):
        a = GeneratedPlaylist(self.type, self.ready, self.notify, playlist)
        b = GeneratedPlaylist(self.type, False, self.notify, None)
        c = GeneratedPlaylist(self.type, self.ready, self.notify, playlist)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
