from yandex_music import Cover


class TestCover:
    type = 'pic'
    uri = 'avatars.yandex.net/get-music-user-playlist/38125/q0ahkhfQE3neTk/%%?1572609906461'
    items_uri = None
    dir = '/get-music-user-playlist/34120/pvg900XixWaHcr/'
    version = '1572609906461'
    custom = True
    prefix = None
    error = None

    def test_expected_values(self, cover):
        assert cover.type == self.type
        assert cover.uri == self.uri
        assert cover.items_uri == self.items_uri
        assert cover.dir == self.dir
        assert cover.version == self.version
        assert cover.custom == self.custom
        assert cover.prefix == self.prefix
        assert cover.error == self.error

    def test_de_json_none(self, client):
        assert Cover.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Cover.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {}
        cover = Cover.de_json(json_dict, client)

    def test_de_json_all(self, client):
        json_dict = {'type_': self.type, 'uri': self.uri, 'items_uri': self.items_uri, 'dir_': self.dir,
                     'version': self.version, 'custom': self.custom, 'prefix': self.prefix, 'error': self.error}
        cover = Cover.de_json(json_dict, client)

        assert cover.type == self.type
        assert cover.uri == self.uri
        assert cover.items_uri == self.items_uri
        assert cover.dir == self.dir
        assert cover.version == self.version
        assert cover.custom == self.custom
        assert cover.prefix == self.prefix
        assert cover.error == self.error

    def test_equality(self, images):
        a = Cover(self.type, self.uri, self.items_uri)

        assert a != images
        assert hash(a) != hash(images)
        assert a is not images
