from yandex_music import ContentRestrictions


class TestContentRestrictions:
    available = True
    disclaimers = ['foreignAgent', 'explicit']

    def test_expected_values(self, content_restrictions):
        assert content_restrictions.available == self.available
        assert content_restrictions.disclaimers == self.disclaimers

    def test_de_json_none(self, client):
        assert ContentRestrictions.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'available': self.available,
            'disclaimers': self.disclaimers,
        }
        content_restrictions = ContentRestrictions.de_json(json_dict, client)

        assert content_restrictions.available == self.available
        assert content_restrictions.disclaimers == self.disclaimers

    def test_equality(self):
        a = ContentRestrictions(available=self.available, disclaimers=self.disclaimers)
        b = ContentRestrictions(available=False, disclaimers=[])
        c = ContentRestrictions(available=self.available, disclaimers=self.disclaimers)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
