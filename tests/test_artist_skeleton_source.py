from yandex_music import ArtistSkeletonSource


class TestArtistSkeletonSource:
    uri = '/artists/12345/tracks'
    count_web = 0
    count = 0

    def test_expected_value(self, artist_skeleton_source):
        assert artist_skeleton_source.uri == self.uri
        assert artist_skeleton_source.count_web == self.count_web
        assert artist_skeleton_source.count == self.count

    def test_de_json_none(self, client):
        assert ArtistSkeletonSource.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'uri': self.uri,
            'countWeb': self.count_web,
            'count': self.count,
        }
        obj = ArtistSkeletonSource.de_json(json_dict, client)

        assert obj.uri == self.uri
        assert obj.count_web == self.count_web
        assert obj.count == self.count

    def test_equality(self):
        a = ArtistSkeletonSource(uri='/artists/12345/tracks')
        b = ArtistSkeletonSource(uri='/artists/67890/tracks')
        c = ArtistSkeletonSource(uri='/artists/12345/tracks')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
