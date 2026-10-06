from typing import Dict

from yandex_music import Client, JSONType, ShotData, ShotType


class TestShotData:
    cover_uri = 'avatars.mds.yandex.net/get-music-misc/49997/img.5da435f1da39b871a74270e2/%%'
    mds_url = 'https://storage.mds.yandex.net/get-music/1634376/public/shots/1036797_1574621686'
    shot_text = 'Бард - это не просто певец, это поющий поэт.'

    def test_expected_values(self, shot_data: ShotData, shot_type: ShotType) -> None:
        assert shot_data.cover_uri == self.cover_uri
        assert shot_data.mds_url == self.mds_url
        assert shot_data.shot_text == self.shot_text
        assert shot_data.shot_type == shot_type

    def test_de_json_none(self, client: Client) -> None:
        assert ShotData.de_json({}, client) is None

    def test_de_json_required(self, client: Client, shot_type: ShotType) -> None:
        json_dict: Dict[str, JSONType] = {
            'cover_uri': self.cover_uri,
            'mds_url': self.mds_url,
            'shot_text': self.shot_text,
            'shot_type': shot_type.to_dict(),
        }
        shot_data = ShotData.de_json(json_dict, client)
        assert shot_data is not None

        assert shot_data.cover_uri == self.cover_uri
        assert shot_data.mds_url == self.mds_url
        assert shot_data.shot_text == self.shot_text
        assert shot_data.shot_type == shot_type

    def test_de_json_all(self, client: Client, shot_type: ShotType) -> None:
        json_dict: Dict[str, JSONType] = {
            'cover_uri': self.cover_uri,
            'mds_url': self.mds_url,
            'shot_text': self.shot_text,
            'shot_type': shot_type.to_dict(),
        }
        shot_data = ShotData.de_json(json_dict, client)
        assert shot_data is not None

        assert shot_data.cover_uri == self.cover_uri
        assert shot_data.mds_url == self.mds_url
        assert shot_data.shot_text == self.shot_text
        assert shot_data.shot_type == shot_type

    def test_equality(self, shot_type: ShotType) -> None:
        a = ShotData(self.cover_uri, self.mds_url, self.shot_text, shot_type)
        b = ShotData('', self.mds_url, self.shot_text, shot_type)
        c = ShotData(self.cover_uri, '', self.shot_text, shot_type)
        d = ShotData(self.cover_uri, self.mds_url, self.shot_text, shot_type)

        assert a != b != c != d
        assert hash(a) != hash(b) != hash(c) != hash(d)
        assert a is not b is not c is not d

        assert a == d
        assert hash(a) == hash(d)
