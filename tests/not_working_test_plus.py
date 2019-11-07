from yandex_music import Plus


class TestPlus:
    has_plus = None
    is_tutorial_completed = None

    def test_expected_values(self, plus):
        assert plus.has_plus == self.has_plus
        assert plus.is_tutorial_completed == self.is_tutorial_completed

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
        pass
