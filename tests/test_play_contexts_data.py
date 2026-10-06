from typing import Dict

from yandex_music import Client, JSONType, PlayContextsData, TrackShortOld


class TestPlayContextsData:
    def test_expected_values(self, play_contexts_data: PlayContextsData, track_short_old: TrackShortOld) -> None:
        assert play_contexts_data.other_tracks == [track_short_old]

    def test_de_json_none(self, client: Client) -> None:
        assert PlayContextsData.de_json({}, client) is None

    def test_de_json_required(self, client: Client, track_short_old: TrackShortOld) -> None:
        json_dict: Dict[str, JSONType] = {'other_tracks': [track_short_old.to_dict()]}
        play_contexts_data = PlayContextsData.de_json(json_dict, client)
        assert play_contexts_data is not None

        assert play_contexts_data.other_tracks == [track_short_old]

    def test_de_json_all(self, client: Client, track_short_old: TrackShortOld) -> None:
        json_dict: Dict[str, JSONType] = {'other_tracks': [track_short_old.to_dict()]}
        play_contexts_data = PlayContextsData.de_json(json_dict, client)
        assert play_contexts_data is not None

        assert play_contexts_data.other_tracks == [track_short_old]

    def test_equality(self, track_short_old: TrackShortOld) -> None:
        a = PlayContextsData([track_short_old])
        b = PlayContextsData([])

        assert a != b != track_short_old
        assert hash(a) != hash(b) != hash(track_short_old)
        assert a is not track_short_old
