from yandex_music import ArtistClips


class TestArtistClips:
    def test_expected_value(self, artist_clips, artist_clip_item, pager):
        assert artist_clips.items == [artist_clip_item]
        assert artist_clips.pager == pager

    def test_de_json_none(self, client):
        assert ArtistClips.de_json({}, client) is None

    def test_de_json_all(self, client, artist_clip_item, pager):
        json_dict = {
            'items': [artist_clip_item.to_dict()],
            'pager': pager.to_dict(),
        }
        obj = ArtistClips.de_json(json_dict, client)

        assert obj.items == [artist_clip_item]
        assert obj.pager == pager

    def test_equality(self, artist_clip_item, pager):
        a = ArtistClips(items=[artist_clip_item], pager=pager)
        b = ArtistClips(items=None, pager=None)
        c = ArtistClips(items=[artist_clip_item], pager=pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
