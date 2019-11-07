from yandex_music import Best


class TestBest:
    type = None
    result = None
    text = None

    def test_expected_values(self, best):
        assert best.type == self.type
        assert best.result == self.result
        assert best.text == self.text

    def test_de_json_required(self, client):
        json_dict = {'type': self.type, 'result': self.result}
        best = Best.de_json(json_dict, client)

        assert best.type == self.type
        assert best.result == self.result

    def test_de_json_all(self, client):
        json_dict = {'type': self.type, 'result': self.result, 'text': self.text}
        best = Best.de_json(json_dict, client)

        assert best.type == self.type
        assert best.result == self.result
        assert best.text == self.text

    def test_equality(self):
        pass
