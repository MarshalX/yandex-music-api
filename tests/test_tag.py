from yandex_music import Tag


class TestTag:
    id_ = '5795ce8f77d30f7fda41bca0'
    value = 'вечные хиты'
    name = 'Вечные хиты'
    og_description = ''
    og_image = 'https://avatars.yandex.net/get-music-misc/2419084/PlaylistTag.5ea7e04c71ca3b6c946af177.ru.og/orig'

    def test_expected_values(self, tag):
        assert tag.id == self.id_
        assert tag.value == self.value
        assert tag.name == self.name
        assert tag.og_description == self.og_description
        assert tag.og_image == self.og_image

    def test_de_json_none(self, client):
        assert Tag.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'id': self.id_, 'value': self.value, 'name': self.name, 'og_description': self.og_description}
        tag = Tag.de_json(json_dict, client)

        assert tag.id == self.id_
        assert tag.value == self.value
        assert tag.name == self.name
        assert tag.og_description == self.og_description

    def test_de_json_all(self, client):
        json_dict = {
            'id': self.id_,
            'value': self.value,
            'name': self.name,
            'og_description': self.og_description,
            'og_image': self.og_image,
        }
        tag = Tag.de_json(json_dict, client)

        assert tag.id == self.id_
        assert tag.value == self.value
        assert tag.name == self.name
        assert tag.og_description == self.og_description
        assert tag.og_image == self.og_image

    def test_equality(self):
        a = Tag(self.id_, self.value, self.name, self.og_description)
        b = Tag('10b300', self.value, self.name, self.og_description)
        c = Tag(self.id_, self.value, '', self.og_description)
        d = Tag(self.id_, self.value, self.name, self.og_description)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
