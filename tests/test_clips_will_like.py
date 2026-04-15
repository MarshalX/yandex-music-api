from yandex_music import ClipsWillLike


class TestClipsWillLike:
    def test_expected_value(self, clips_will_like, clip, pager):
        assert clips_will_like.clips == [clip]
        assert clips_will_like.pager == pager

    def test_de_json_none(self, client):
        assert ClipsWillLike.de_json({}, client) is None

    def test_de_json_all(self, client, clip, pager):
        json_dict = {
            'clips': [clip.to_dict()],
            'pager': pager.to_dict(),
        }
        clips_will_like = ClipsWillLike.de_json(json_dict, client)

        assert clips_will_like.clips == [clip]
        assert clips_will_like.pager == pager

    def test_equality(self, clip, pager):
        a = ClipsWillLike(clips=[clip], pager=pager)
        b = ClipsWillLike(clips=None, pager=None)
        c = ClipsWillLike(clips=[clip], pager=pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
