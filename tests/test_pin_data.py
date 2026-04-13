from yandex_music import PinData


class TestPinData:
    id = 12345
    uid = 100500
    kind = 3
    playlist_uuid = 'lk.a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    name = 'Test Artist'
    title = 'Test Album'

    def test_expected_values_artist(self, pin_data_artist, cover, content_restrictions):
        assert pin_data_artist.id == self.id
        assert pin_data_artist.name == self.name
        assert pin_data_artist.cover == cover
        assert pin_data_artist.content_restrictions == content_restrictions

    def test_expected_value_album(self, pin_data_album, cover, content_restrictions):
        assert pin_data_album.id == self.id
        assert pin_data_album.title == self.title
        assert pin_data_album.cover == cover
        assert pin_data_album.content_restrictions == content_restrictions

    def test_expected_value_playlist(self, pin_data_playlist, cover):
        assert pin_data_playlist.uid == self.uid
        assert pin_data_playlist.kind == self.kind
        assert pin_data_playlist.playlist_uuid == self.playlist_uuid
        assert pin_data_playlist.title == self.title
        assert pin_data_playlist.cover == cover

    def test_de_json_none(self, client):
        assert PinData.de_json({}, client) is None

    def test_de_json_artist(self, client, cover, content_restrictions):
        json_dict = {
            'id': self.id,
            'name': self.name,
            'cover': cover.to_dict(),
            'contentRestrictions': content_restrictions.to_dict(),
        }
        pin_data = PinData.de_json(json_dict, client)

        assert pin_data.id == self.id
        assert pin_data.name == self.name
        assert pin_data.content_restrictions == content_restrictions

    def test_de_json_playlist(self, client, cover):
        json_dict = {
            'uid': self.uid,
            'kind': self.kind,
            'playlistUuid': self.playlist_uuid,
            'title': self.title,
            'cover': cover.to_dict(),
        }
        pin_data = PinData.de_json(json_dict, client)

        assert pin_data.uid == self.uid
        assert pin_data.kind == self.kind
        assert pin_data.playlist_uuid == self.playlist_uuid
        assert pin_data.title == self.title

    def test_equality(self, cover):
        a = PinData(id=self.id, name=self.name, cover=cover)
        b = PinData(id=999, name='Other', cover=cover)
        c = PinData(id=self.id, name=self.name, cover=cover)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
