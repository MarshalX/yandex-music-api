from yandex_music import Operator


class TestOperator:
    product_id = 'bz.649'
    phone = '+998905555555'
    payment_regularity = 'Списание средств производится\nавтоматически каждый день'
    title = 'Maxsus taklif!'
    suspended = False

    def test_expected_values(self, operator, deactivation):
        assert operator.product_id == self.product_id
        assert operator.phone == self.phone
        assert operator.payment_regularity == self.payment_regularity
        assert operator.deactivation == [deactivation]
        assert operator.title == self.title
        assert operator.suspended == self.suspended

    def test_de_json_none(self, client):
        assert Operator.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Operator.de_list({}, client) == []

    def test_de_json_required(self, client, deactivation):
        json_dict = {
            'product_id': self.product_id,
            'phone': self.phone,
            'payment_regularity': self.payment_regularity,
            'deactivation': [deactivation.to_dict()],
            'title': self.title,
            'suspended': self.suspended,
        }
        operator = Operator.de_json(json_dict, client)

        assert operator.product_id == self.product_id
        assert operator.phone == self.phone
        assert operator.payment_regularity == self.payment_regularity
        assert operator.deactivation == [deactivation]
        assert operator.title == self.title
        assert operator.suspended == self.suspended

    def test_de_json_all(self, client, deactivation):
        json_dict = {
            'product_id': self.product_id,
            'phone': self.phone,
            'payment_regularity': self.payment_regularity,
            'deactivation': [deactivation.to_dict()],
            'title': self.title,
            'suspended': self.suspended,
        }
        operator = Operator.de_json(json_dict, client)

        assert operator.product_id == self.product_id
        assert operator.phone == self.phone
        assert operator.payment_regularity == self.payment_regularity
        assert operator.deactivation == [deactivation]
        assert operator.title == self.title
        assert operator.suspended == self.suspended

    def test_equality(self, deactivation):
        a = Operator(self.product_id, self.phone, self.payment_regularity, [deactivation], self.title, self.suspended)
        b = Operator('', self.phone, self.payment_regularity, [deactivation], self.title, self.suspended)
        c = Operator(self.product_id, self.phone, self.payment_regularity, [deactivation], self.title, self.suspended)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
