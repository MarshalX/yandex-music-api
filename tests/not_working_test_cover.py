from yandex_music import Cover


class TestCover:
    type = None
    uri = None
    items_uri = None
    dir = None
    version = None
    custom = None
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

    def test_de_json_required(self, client):
        json_dict = {}
        cover = Cover.de_json(json_dict, client)

    def test_de_json_all(self, client):
        json_dict = {'type': self.type, 'uri': self.uri, 'items_uri': self.items_uri, 'dir': self.dir,
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

    def test_equality(self):
        pass
