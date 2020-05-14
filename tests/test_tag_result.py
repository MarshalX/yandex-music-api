import pytest

from yandex_music import TagResult


@pytest.fixture(scope='class')
def tag_result(tag, playlist_id):
    return TagResult(tag, [playlist_id])


class TestTagResult:
    def test_expected_values(self, tag_result, tag, playlist_id):
        assert tag_result.tag == tag
        assert tag_result.ids == [playlist_id]

    def test_de_json_none(self, client):
        assert TagResult.de_json({}, client) is None

    def test_de_json_required(self, client, tag, playlist_id):
        json_dict = {'tag': tag.to_dict(), 'ids': [playlist_id.to_dict()]}
        tag_result = TagResult.de_json(json_dict, client)

        assert tag_result.tag == tag
        assert tag_result.ids == [playlist_id]

    def test_de_json_all(self, client, tag, playlist_id):
        json_dict = {'tag': tag.to_dict(), 'ids': [playlist_id.to_dict()]}
        tag_result = TagResult.de_json(json_dict, client)

        assert tag_result.tag == tag
        assert tag_result.ids == [playlist_id]

    def test_equality(self, tag, playlist_id):
        a = TagResult(tag, [playlist_id])
        b = TagResult(tag, [])
        c = TagResult(tag, [playlist_id])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
