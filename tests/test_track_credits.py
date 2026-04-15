from yandex_music import TrackCredits


class TestTrackCredits:
    def test_expected_value(self, track_credits, track_credit):
        assert track_credits.credits == [track_credit]

    def test_de_json_none(self, client):
        assert TrackCredits.de_json({}, client) is None

    def test_de_json_all(self, client, track_credit):
        json_dict = {
            'credits': [track_credit.to_dict()],
        }
        track_credits = TrackCredits.de_json(json_dict, client)

        assert track_credits.credits == [track_credit]

    def test_equality(self, track_credit):
        a = TrackCredits(credits=[track_credit])
        b = TrackCredits(credits=None)
        c = TrackCredits(credits=[track_credit])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
