from yandex_music import Label


class TestLabel:
    id = 148217
    name = 'tommee profitt STUDIOS'
    description = 'Лейбл с Американской Саунд-машины'
    description_formatted = 'Форматированное описание'
    image = 'avatars.yandex.net/get-music-misc/12345/label.148217.image/%%'
    type = 'musical'

    another_representation_of_label = 'NoCopyrightSounds'

    def test_expected_values(self, label, link):
        if isinstance(label, str):
            assert label == self.another_representation_of_label
        else:
            assert label.id == self.id
            assert label.name == self.name
            assert label.description == self.description
            assert label.description_formatted == self.description_formatted
            assert label.image == self.image
            assert label.links == [link]
            assert label.type == self.type

    def test_de_list_none(self, client):
        assert Label.de_list([], client) == []

    def test_de_list_strings(self, client):
        data = ['First', 'Second']
        assert Label.de_list(data, client) == data

    def test_de_json_none(self, client):
        assert Label.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'id': self.id, 'name': self.name}
        label = Label.de_json(json_dict, client)

        assert label.id == self.id
        assert label.name == self.name
        assert label.description is None
        assert label.description_formatted is None
        assert label.image is None
        assert label.links == []
        assert label.type is None

    def test_de_json_all(self, client, link):
        json_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'descriptionFormatted': self.description_formatted,
            'image': self.image,
            'links': [link.to_dict()],
            'type': self.type,
        }
        label = Label.de_json(json_dict, client)

        assert label.id == self.id
        assert label.name == self.name
        assert label.description == self.description
        assert label.description_formatted == self.description_formatted
        assert label.image == self.image
        assert label.links == [link]
        assert label.type == self.type

    def test_equality(self):
        a = Label(self.id, self.name)
        b = Label(10, self.name)
        c = Label(self.id, '')
        d = Label(self.id, self.name)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
