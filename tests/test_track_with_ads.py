from typing import Dict

from yandex_music import Client, JSONType, Track, TrackWithAds


class TestTrackWithAds:
    type = 'track'

    def test_expected_values(self, track_with_ads: TrackWithAds, track: Track) -> None:
        assert track_with_ads.type == self.type
        assert track_with_ads.track == track

    def test_de_json_none(self, client: Client) -> None:
        assert TrackWithAds.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert TrackWithAds.de_list([], client) == []

    def test_de_json_required(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type, 'track': track.to_dict()}
        track_with_ads = TrackWithAds.de_json(json_dict, client)
        assert track_with_ads is not None

        assert track_with_ads.type == self.type
        assert track_with_ads.track == track

    def test_de_json_all(self, client: Client, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type, 'track': track.to_dict()}
        track_with_ads = TrackWithAds.de_json(json_dict, client)
        assert track_with_ads is not None

        assert track_with_ads.type == self.type
        assert track_with_ads.track == track

    def test_equality(self, track: Track) -> None:
        a = TrackWithAds(self.type, track)
        b = TrackWithAds('', track)
        c = TrackWithAds(self.type, track)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
