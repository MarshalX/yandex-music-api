from yandex_music import Subscription


class TestSubscription:
    can_start_trial = None
    mcdonalds = None
    end = None

    def test_expected_values(self, subscription, auto_renewable):
        assert subscription.auto_renewable == auto_renewable
        assert subscription.can_start_trial == self.can_start_trial
        assert subscription.mcdonalds == self.mcdonalds
        assert subscription.end == self.end

    def test_de_json_required(self, client):
        json_dict = {}
        subscription = Subscription.de_json(json_dict, client)

    def test_de_json_all(self, client, auto_renewable):
        json_dict = {'auto_renewable': auto_renewable, 'can_start_trial': self.can_start_trial,
                     'mcdonalds': self.mcdonalds, 'end': self.end}
        subscription = Subscription.de_json(json_dict, client)

        assert subscription.auto_renewable == auto_renewable
        assert subscription.can_start_trial == self.can_start_trial
        assert subscription.mcdonalds == self.mcdonalds
        assert subscription.end == self.end

    def test_equality(self):
        pass
