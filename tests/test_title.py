from yandex_music import Title


class TestTitle:
    title = 'Hammasi'
    full_title = 'Barcha janrlar musiqasi'

    def test_expected_values(self, title):
        assert title.title == self.title
        assert title.full_title == self.full_title

    def test_de_json_none(self, client):
        assert Title.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'title': self.title}
        title = Title.de_json(json_dict, client)

        assert title.title == self.title

    def test_de_json_all(self, client):
        json_dict = {'title': self.title, 'full_title': self.full_title}
        title = Title.de_json(json_dict, client)

        assert title.title == self.title
        assert title.full_title == self.full_title

    def test_equality(self):
        a = Title(self.title, self.full_title)
        b = Title('')
        c = Title(self.title, self.full_title)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
