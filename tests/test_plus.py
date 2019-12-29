from yandex_music import Plus


class TestPlus:
    has_plus = True
    is_tutorial_completed = True

    def test_expected_values(self, plus):
        assert plus.has_plus == self.has_plus
        assert plus.is_tutorial_completed == self.is_tutorial_completed

    def test_de_json_none(self, client):
        assert Plus.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'has_plus': self.has_plus, 'is_tutorial_completed': self.is_tutorial_completed}
        plus = Plus.de_json(json_dict, client)

        assert plus.has_plus == self.has_plus
        assert plus.is_tutorial_completed == self.is_tutorial_completed

    def test_de_json_all(self, client):
        json_dict = {'has_plus': self.has_plus, 'is_tutorial_completed': self.is_tutorial_completed}
        plus = Plus.de_json(json_dict, client)

        assert plus.has_plus == self.has_plus
        assert plus.is_tutorial_completed == self.is_tutorial_completed

    def test_equality(self):
        a = Plus(self.has_plus, self.is_tutorial_completed)
        b = Plus(self.has_plus, False)
        c = Plus(self.has_plus, self.is_tutorial_completed)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
