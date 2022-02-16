from yandex_music import Context


class TestContext:
    type_ = 'playlist'
    id_ = '503646255:69814820'
    description = 'Playlist of the Day'

    def test_expected_values(self, context):
        assert context.type == self.type_
        assert context.id == self.id_
        assert context.description == self.description

    def test_de_json_none(self, client):
        assert Context.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'type': self.type_}
        context = Context.de_json(json_dict, client)

        assert context.type == self.type_

    def test_de_json_all(self, client, track_id):
        json_dict = {'type': self.type_, 'id': self.id_, 'description': self.description}
        context = Context.de_json(json_dict, client)

        assert context.type == self.type_
        assert context.id == self.id_
        assert context.description == self.description

    def test_equality(self):
        a = Context(self.type_)
        b = Context('')
        c = Context(self.type_)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
