from typing import Dict

import pytest

from yandex_music import Client, JSONType, PlaylistId, Tag, TagResult


@pytest.fixture(scope='class')
def tag_result(tag: Tag, playlist_id: PlaylistId) -> TagResult:
    return TagResult([playlist_id], tag)


class TestTagResult:
    def test_expected_values(self, tag_result: TagResult, tag: Tag, playlist_id: PlaylistId) -> None:
        assert tag_result.tag == tag
        assert tag_result.ids == [playlist_id]

    def test_de_json_none(self, client: Client) -> None:
        assert TagResult.de_json({}, client) is None

    def test_de_json_required(self, playlist_id: PlaylistId) -> None:
        json_dict: Dict[str, JSONType] = {'ids': [playlist_id.to_dict()]}
        tag_result = TagResult.de_json(json_dict, Client(strict=True))
        assert tag_result is not None

        assert tag_result.tag is None
        assert tag_result.ids == [playlist_id]

    def test_de_json_all(self, client: Client, tag: Tag, playlist_id: PlaylistId) -> None:
        json_dict: Dict[str, JSONType] = {'tag': tag.to_dict(), 'ids': [playlist_id.to_dict()]}
        tag_result = TagResult.de_json(json_dict, client)
        assert tag_result is not None

        assert tag_result.tag == tag
        assert tag_result.ids == [playlist_id]

    def test_equality(self, tag: Tag, playlist_id: PlaylistId) -> None:
        a = TagResult([playlist_id], tag)
        b = TagResult([], tag)
        c = TagResult([playlist_id], tag)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
