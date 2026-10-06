from typing import Dict

from yandex_music import Artist, ArtistClipData, Client, Clip, JSONType


class TestArtistClipData:
    def test_expected_value(self, artist_clip_data: ArtistClipData, clip: Clip, artist: Artist) -> None:
        assert artist_clip_data.clip == clip
        assert artist_clip_data.artists == [artist]

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistClipData.de_json({}, client) is None

    def test_de_json_all(self, client: Client, clip: Clip, artist: Artist) -> None:
        json_dict: Dict[str, JSONType] = {
            'clip': clip.to_dict(),
            'artists': [artist.to_dict()],
        }
        obj = ArtistClipData.de_json(json_dict, client)
        assert obj is not None

        assert obj.clip == clip
        assert obj.artists == [artist]

    def test_equality(self, clip: Clip) -> None:
        a = ArtistClipData(clip=clip)
        b = ArtistClipData(clip=None)
        c = ArtistClipData(clip=clip)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
