from yandex_music import Value


class TestValue:
    value = 'not-russian'
    name = 'Иностранный'
    image_url = 'https://avatars.mds.yandex.net/get-music-misc/12345/img.fake/orig'
    serialized_seed = 'settingLanguage:not-russian'
    unspecified = False

    def test_expected_values(self, value):
        assert value.value == self.value
        assert value.name == self.name
        assert value.image_url == self.image_url
        assert value.serialized_seed == self.serialized_seed
        assert value.unspecified == self.unspecified

    def test_de_json_none(self, client):
        assert Value.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Value.de_list([], client) == []

    def test_de_json_required(self, client):
        json_dict = {'value': self.value, 'name': self.name}
        value = Value.de_json(json_dict, client)

        assert value.value == self.value
        assert value.name == self.name

    def test_de_json_all(self, client):
        json_dict = {
            'value': self.value,
            'name': self.name,
            'imageUrl': self.image_url,
            'serializedSeed': self.serialized_seed,
            'unspecified': self.unspecified,
        }
        value = Value.de_json(json_dict, client)

        assert value.value == self.value
        assert value.name == self.name
        assert value.image_url == self.image_url
        assert value.serialized_seed == self.serialized_seed
        assert value.unspecified == self.unspecified

    def test_de_json_scale_value(self, client):
        value = Value.de_json({'value': 4, 'name': 'Веселее'}, client)

        assert value.value == 4

    def test_equality(self):
        a = Value(self.value, self.name)
        b = Value(self.value, '')
        c = Value(self.value, self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
