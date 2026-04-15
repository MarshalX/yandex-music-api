from yandex_music import ArtistInfo


class TestArtistInfo:
    likes_count = 100500
    description = 'Fake artist description'
    artist_type = 'artist'

    def test_expected_value(self, artist_info, artist, stats, artist_trailer_status, cover):
        assert artist_info.artist == artist
        assert artist_info.likes_count == self.likes_count
        assert artist_info.stats == stats
        assert artist_info.trailer == artist_trailer_status
        assert artist_info.covers == [cover]
        assert artist_info.description == self.description
        assert artist_info.artist_type == self.artist_type

    def test_de_json_none(self, client):
        assert ArtistInfo.de_json({}, client) is None

    def test_de_json_all(self, client, artist, stats, artist_trailer_status, cover):
        json_dict = {
            'artist': artist.to_dict(),
            'likesCount': self.likes_count,
            'stats': stats.to_dict(),
            'trailer': artist_trailer_status.to_dict(),
            'covers': [cover.to_dict()],
            'description': self.description,
            'artistType': self.artist_type,
        }
        obj = ArtistInfo.de_json(json_dict, client)

        assert obj.artist == artist
        assert obj.likes_count == self.likes_count
        assert obj.description == self.description

    def test_equality(self, artist):
        a = ArtistInfo(artist=artist)
        b = ArtistInfo(artist=None)
        c = ArtistInfo(artist=artist)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
