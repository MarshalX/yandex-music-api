from yandex_music import ArtistClipData


class TestArtistClipData:
    def test_expected_value(self, artist_clip_data, clip, artist):
        assert artist_clip_data.clip == clip
        assert artist_clip_data.artists == [artist]

    def test_de_json_none(self, client):
        assert ArtistClipData.de_json({}, client) is None

    def test_de_json_all(self, client, clip, artist):
        json_dict = {
            'clip': clip.to_dict(),
            'artists': [artist.to_dict()],
        }
        obj = ArtistClipData.de_json(json_dict, client)

        assert obj.clip == clip
        assert obj.artists == [artist]

    def test_equality(self, clip):
        a = ArtistClipData(clip=clip)
        b = ArtistClipData(clip=None)
        c = ArtistClipData(clip=clip)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
