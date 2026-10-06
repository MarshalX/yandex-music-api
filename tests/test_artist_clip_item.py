from typing import Dict

from yandex_music import ArtistClipData, ArtistClipItem, Client, JSONType


class TestArtistClipItem:
    type = 'clip'

    def test_expected_value(self, artist_clip_item: ArtistClipItem, artist_clip_data: ArtistClipData) -> None:
        assert artist_clip_item.type == self.type
        assert artist_clip_item.data == artist_clip_data

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistClipItem.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist_clip_data: ArtistClipData) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'data': artist_clip_data.to_dict(),
        }
        obj = ArtistClipItem.de_json(json_dict, client)
        assert obj is not None

        assert obj.type == self.type
        assert obj.data == artist_clip_data

    def test_equality(self, artist_clip_data: ArtistClipData) -> None:
        a = ArtistClipItem(type='clip', data=artist_clip_data)
        b = ArtistClipItem(type='clip', data=None)
        c = ArtistClipItem(type='clip', data=artist_clip_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
