from yandex_music import Credits


class TestCredits:
    def test_expected_value(self, credits_, credit):
        assert credits_.credits == [credit]

    def test_de_json_none(self, client):
        assert Credits.de_json({}, client) is None

    def test_de_json_all(self, client, credit):
        json_dict = {
            'credits': [credit.to_dict()],
        }
        credits_ = Credits.de_json(json_dict, client)

        assert credits_.credits == [credit]

    def test_equality(self, credit):
        a = Credits(credits=[credit])
        b = Credits(credits=None)
        c = Credits(credits=[credit])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
