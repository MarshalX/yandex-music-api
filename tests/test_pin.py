from typing import Dict, List

from tests.test_pin_data import TestPinData
from yandex_music import Client, ContentRestrictions, Cover, JSONType, Pin, PinData


class TestPin:
    type_artist = 'artist_item'
    type_album = 'album_item'
    type_playlist = 'playlist_item'

    def test_expected_value_artist(self, pin_artist: Pin, pin_data_artist: PinData) -> None:
        assert pin_artist.type == self.type_artist
        assert pin_artist.data == pin_data_artist

    def test_expected_value_album(self, pin_album: Pin, pin_data_album: PinData) -> None:
        assert pin_album.type == self.type_album
        assert pin_album.data == pin_data_album

    def test_expected_value_playlist(self, pin_playlist: Pin, pin_data_playlist: PinData) -> None:
        assert pin_playlist.type == self.type_playlist
        assert pin_playlist.data == pin_data_playlist

    def test_de_json_none(self, client: Client) -> None:
        assert Pin.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Pin.de_list([], client) == []

    def test_de_json_artist(self, client: Client, cover: Cover, content_restrictions: ContentRestrictions) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type_artist,
            'data': {
                'id': TestPinData.id,
                'name': TestPinData.name,
                'cover': cover.to_dict(),
                'contentRestrictions': content_restrictions.to_dict(),
            },
        }
        pin = Pin.de_json(json_dict, client)
        assert pin is not None

        assert pin.type == self.type_artist
        assert pin.data is not None
        assert pin.data.id == TestPinData.id
        assert pin.data.name == TestPinData.name

    def test_de_list(self, client: Client, cover: Cover) -> None:
        json_list: List[JSONType] = [
            {
                'type': self.type_artist,
                'data': {
                    'id': TestPinData.id,
                    'name': TestPinData.name,
                    'cover': cover.to_dict(),
                },
            },
            {
                'type': self.type_album,
                'data': {
                    'id': TestPinData.id,
                    'title': TestPinData.title,
                    'cover': cover.to_dict(),
                },
            },
        ]
        pins = Pin.de_list(json_list, client)

        assert len(pins) == 2
        assert pins[0].type == self.type_artist
        assert pins[1].type == self.type_album

    def test_equality(self, pin_data_artist: PinData) -> None:
        a = Pin(type=self.type_artist, data=pin_data_artist)
        b = Pin(type=self.type_album, data=pin_data_artist)
        c = Pin(type=self.type_artist, data=pin_data_artist)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
