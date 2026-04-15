from yandex_music import TrailerInfo


class TestTrailerInfo:
    title = 'Трейлер альбома'

    def test_expected_values(self, trailer_info, track):
        assert trailer_info.title == self.title
        assert trailer_info.tracks == [track]

    def test_de_json_none(self, client):
        assert TrailerInfo.de_json({}, client) is None

    def test_de_json_all(self, client, track):
        json_dict = {
            'title': self.title,
            'tracks': [track.to_dict()],
        }
        info = TrailerInfo.de_json(json_dict, client)

        assert info.title == self.title
        assert info.tracks == [track]

    def test_equality(self, track):
        a = TrailerInfo(title=self.title, tracks=[track])
        b = TrailerInfo(title='Other', tracks=[track])
        c = TrailerInfo(title=self.title, tracks=[track])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
