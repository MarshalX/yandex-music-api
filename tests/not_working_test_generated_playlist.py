import pytest

from yandex_music import GeneratedPlaylist


@pytest.fixture(scope='class')
def generated_playlist(data):
    return GeneratedPlaylist(TestGeneratedPlaylist.type, TestGeneratedPlaylist.ready, TestGeneratedPlaylist.notify,
                             data)


class TestGeneratedPlaylist:
    type = None
    ready = None
    notify = None

    def test_expected_values(self, generated_playlist, data):
        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == data

    def test_de_json_required(self, client, data):
        json_dict = {'type': self.type, 'ready': self.ready, 'notify': self.notify, 'data': data}
        generated_playlist = GeneratedPlaylist.de_json(json_dict, client)

        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == data

    def test_de_json_all(self, client, data):
        json_dict = {'type': self.type, 'ready': self.ready, 'notify': self.notify, 'data': data}
        generated_playlist = GeneratedPlaylist.de_json(json_dict, client)

        assert generated_playlist.type == self.type
        assert generated_playlist.ready == self.ready
        assert generated_playlist.notify == self.notify
        assert generated_playlist.data == data

    def test_equality(self):
        pass
