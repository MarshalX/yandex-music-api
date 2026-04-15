from yandex_music import ArtistClipItem


class TestArtistClipItem:
    type = 'clip'

    def test_expected_value(self, artist_clip_item, artist_clip_data):
        assert artist_clip_item.type == self.type
        assert artist_clip_item.data == artist_clip_data

    def test_de_json_none(self, client):
        assert ArtistClipItem.de_json({}, client) is None

    def test_de_json_all(self, client, artist_clip_data):
        json_dict = {
            'type': self.type,
            'data': artist_clip_data.to_dict(),
        }
        obj = ArtistClipItem.de_json(json_dict, client)

        assert obj.type == self.type
        assert obj.data == artist_clip_data

    def test_equality(self, artist_clip_data):
        a = ArtistClipItem(type='clip', data=artist_clip_data)
        b = ArtistClipItem(type='clip', data=None)
        c = ArtistClipItem(type='clip', data=artist_clip_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
