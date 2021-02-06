from yandex_music import ShotData


class TestShotData:
    cover_uri = 'avatars.mds.yandex.net/get-music-misc/49997/img.5da435f1da39b871a74270e2/%%'
    mds_url = 'https://storage.mds.yandex.net/get-music/1634376/public/shots/1036797_1574621686'
    shot_text = 'Бард - это не просто певец, это поющий поэт.'

    def test_expected_values(self, shot_data, shot_type):
        assert shot_data.cover_uri == self.cover_uri
        assert shot_data.mds_url == self.mds_url
        assert shot_data.shot_text == self.shot_text
        assert shot_data.shot_type == shot_type

    def test_de_json_none(self, client):
        assert ShotData.de_json({}, client) is None

    def test_de_json_required(self, client, shot_type):
        json_dict = {
            'cover_uri': self.cover_uri,
            'mds_url': self.mds_url,
            'shot_text': self.shot_text,
            'shot_type': shot_type.to_dict(),
        }
        shot_data = ShotData.de_json(json_dict, client)

        assert shot_data.cover_uri == self.cover_uri
        assert shot_data.mds_url == self.mds_url
        assert shot_data.shot_text == self.shot_text
        assert shot_data.shot_type == shot_type

    def test_de_json_all(self, client, shot_type):
        json_dict = {
            'cover_uri': self.cover_uri,
            'mds_url': self.mds_url,
            'shot_text': self.shot_text,
            'shot_type': shot_type.to_dict(),
        }
        shot_data = ShotData.de_json(json_dict, client)

        assert shot_data.cover_uri == self.cover_uri
        assert shot_data.mds_url == self.mds_url
        assert shot_data.shot_text == self.shot_text
        assert shot_data.shot_type == shot_type

    def test_equality(self, shot_type):
        a = ShotData(self.cover_uri, self.mds_url, self.shot_text, shot_type)
        b = ShotData('', self.mds_url, self.shot_text, shot_type)
        c = ShotData(self.cover_uri, '', self.shot_text, shot_type)
        d = ShotData(self.cover_uri, self.mds_url, self.shot_text, shot_type)

        assert a != b != c != d
        assert hash(a) != hash(b) != hash(c) != hash(d)
        assert a is not b is not c is not d

        assert a == d
        assert hash(a) == hash(d)
