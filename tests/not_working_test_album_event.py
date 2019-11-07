import pytest

from yandex_music import AlbumEvent


@pytest.fixture(scope='class')
def album_event(album, tracks):
    return AlbumEvent(album, tracks)


class TestAlbumEvent:

    def test_expected_values(self, album_event, album, tracks):
        assert album_event.album == album
        assert album_event.tracks == tracks

    def test_de_json_required(self, client, album, tracks):
        json_dict = {'album': album, 'tracks': tracks}
        album_event = AlbumEvent.de_json(json_dict, client)

        assert album_event.album == album
        assert album_event.tracks == tracks

    def test_de_json_all(self, client, album, tracks):
        json_dict = {'album': album, 'tracks': tracks}
        album_event = AlbumEvent.de_json(json_dict, client)

        assert album_event.album == album
        assert album_event.tracks == tracks

    def test_equality(self):
        pass
