from typing import Dict

from yandex_music import Client, JSONType, Track, TrailerInfo


class TestTrailerInfo:
    title = 'Трейлер альбома'

    def test_expected_values(self, trailer_info: TrailerInfo, track: Track) -> None:
        assert trailer_info.title == self.title
        assert trailer_info.tracks == [track]

    def test_de_json_none(self, client: Client) -> None:
        assert TrailerInfo.de_json({}, client) is None

    def test_de_json_all(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'tracks': [track.to_dict()],
        }
        info = TrailerInfo.de_json(json_dict, client)
        assert info is not None

        assert info.title == self.title
        assert info.tracks == [track]

    def test_equality(self, track: Track) -> None:
        a = TrailerInfo(title=self.title, tracks=[track])
        b = TrailerInfo(title='Other', tracks=[track])
        c = TrailerInfo(title=self.title, tracks=[track])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
