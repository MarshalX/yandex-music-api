from yandex_music import Best


class TestBest:
    type = 'artist'
    text = 'empathy test'

    def test_expected_values(self, best_with_result):
        best, result = best_with_result

        assert best.type == best.type
        assert best.result == result
        assert best.text == self.text

    def test_de_json_none(self, client):
        assert Best.de_json({}, client) is None

    def test_de_json_required(self, client, best_with_result):
        best_fixture, result = best_with_result

        json_dict = {'type': best_fixture.type, 'result': result.to_dict()}
        best = Best.de_json(json_dict, client)

        assert best.type == best_fixture.type
        assert best.result == result

    def test_de_json_all(self, client, best_with_result):
        best_fixture, result = best_with_result

        json_dict = {'type': best_fixture.type, 'result': result.to_dict(), 'text': self.text}
        best = Best.de_json(json_dict, client)

        assert best.type == best_fixture.type
        assert best.result == result
        assert best.text == self.text

    def test_equality(self, best_with_result):
        best, result = best_with_result

        a = Best(best.type, result)
        b = Best(best.type, None)
        c = Best(best.type, result)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
