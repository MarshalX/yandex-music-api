from typing import Dict

from yandex_music import ArtistClipItem, ArtistClips, Client, JSONType, Pager


class TestArtistClips:
    def test_expected_value(self, artist_clips: ArtistClips, artist_clip_item: ArtistClipItem, pager: Pager) -> None:
        assert artist_clips.items == [artist_clip_item]
        assert artist_clips.pager == pager

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistClips.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist_clip_item: ArtistClipItem, pager: Pager) -> None:
        json_dict: Dict[str, JSONType] = {
            'items': [artist_clip_item.to_dict()],
            'pager': pager.to_dict(),
        }
        obj = ArtistClips.de_json(json_dict, client)
        assert obj is not None

        assert obj.items == [artist_clip_item]
        assert obj.pager == pager

    def test_equality(self, artist_clip_item: ArtistClipItem, pager: Pager) -> None:
        a = ArtistClips(items=[artist_clip_item], pager=pager)
        b = ArtistClips(items=None, pager=None)
        c = ArtistClips(items=[artist_clip_item], pager=pager)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
