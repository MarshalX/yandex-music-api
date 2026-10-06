from typing import Dict

from yandex_music import Client, Context, JSONType, TrackId


class TestContext:
    type_ = 'playlist'
    id_ = '503646255:69814820'
    description = 'Playlist of the Day'

    def test_expected_values(self, context: Context) -> None:
        assert context.type == self.type_
        assert context.id == self.id_
        assert context.description == self.description

    def test_de_json_none(self, client: Client) -> None:
        assert Context.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type_}
        context = Context.de_json(json_dict, client)
        assert context is not None

        assert context.type == self.type_

    def test_de_json_all(self, client: Client, track_id: TrackId) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type_, 'id': self.id_, 'description': self.description}
        context = Context.de_json(json_dict, client)
        assert context is not None

        assert context.type == self.type_
        assert context.id == self.id_
        assert context.description == self.description

    def test_equality(self) -> None:
        a = Context(self.type_)
        b = Context('')
        c = Context(self.type_)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
