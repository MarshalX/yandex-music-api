from yandex_music import Subscription


class TestSubscription:
    can_start_trial = False
    mcdonalds = False
    end = None

    def test_expected_values(self, subscription, renewable_remainder, auto_renewable, non_auto_renewable, operator):
        assert subscription.non_auto_renewable_remainder == renewable_remainder
        assert subscription.auto_renewable == [auto_renewable]
        assert subscription.family_auto_renewable == [auto_renewable]
        assert subscription.operator == [operator]
        assert subscription.non_auto_renewable == non_auto_renewable
        assert subscription.can_start_trial == self.can_start_trial
        assert subscription.mcdonalds == self.mcdonalds
        assert subscription.end == self.end

    def test_de_json_none(self, client):
        assert Subscription.de_json({}, client) is None

    def test_de_json_required(self, client, renewable_remainder, auto_renewable):
        json_dict = {
            'non_auto_renewable_remainder': renewable_remainder.to_dict(),
            'auto_renewable': [auto_renewable.to_dict()],
            'family_auto_renewable': [auto_renewable.to_dict()],
        }
        subscription = Subscription.de_json(json_dict, client)

        assert subscription.non_auto_renewable_remainder == renewable_remainder
        assert subscription.auto_renewable == [auto_renewable]
        assert subscription.family_auto_renewable == [auto_renewable]

    def test_de_json_all(self, client, renewable_remainder, auto_renewable, non_auto_renewable, operator):
        json_dict = {
            'auto_renewable': [auto_renewable.to_dict()],
            'can_start_trial': self.can_start_trial,
            'mcdonalds': self.mcdonalds,
            'end': self.end,
            'non_auto_renewable_remainder': renewable_remainder.to_dict(),
            'family_auto_renewable': [auto_renewable.to_dict()],
            'non_auto_renewable': non_auto_renewable.to_dict(),
            'operator': [operator.to_dict()],
        }
        subscription = Subscription.de_json(json_dict, client)

        assert subscription.non_auto_renewable_remainder == renewable_remainder
        assert subscription.auto_renewable == [auto_renewable]
        assert subscription.family_auto_renewable == [auto_renewable]
        assert subscription.operator == [operator]
        assert subscription.non_auto_renewable == non_auto_renewable
        assert subscription.can_start_trial == self.can_start_trial
        assert subscription.mcdonalds == self.mcdonalds
        assert subscription.end == self.end

    def test_equality(self, renewable_remainder, auto_renewable):
        a = Subscription(renewable_remainder, [auto_renewable], [auto_renewable])
        b = Subscription(renewable_remainder, [], [auto_renewable])

        assert a != b != auto_renewable
        assert hash(a) != hash(b) != hash(auto_renewable)
        assert a is not auto_renewable
