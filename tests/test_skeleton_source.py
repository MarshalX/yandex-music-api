from yandex_music import SkeletonSource


class TestSkeletonSource:
    uri = '/artists/12345/tracks'
    count_web = 0
    count = 0

    def test_expected_value(self, skeleton_source):
        assert skeleton_source.uri == self.uri
        assert skeleton_source.count_web == self.count_web
        assert skeleton_source.count == self.count

    def test_de_json_none(self, client):
        assert SkeletonSource.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'uri': self.uri,
            'countWeb': self.count_web,
            'count': self.count,
        }
        obj = SkeletonSource.de_json(json_dict, client)

        assert obj.uri == self.uri
        assert obj.count_web == self.count_web
        assert obj.count == self.count

    def test_equality(self):
        a = SkeletonSource(uri='/artists/12345/tracks')
        b = SkeletonSource(uri='/artists/67890/tracks')
        c = SkeletonSource(uri='/artists/12345/tracks')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
