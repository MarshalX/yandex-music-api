from typing import Dict

from yandex_music import Client, ContentRestrictions, JSONType


class TestContentRestrictions:
    available = True
    disclaimers = ['foreignAgent', 'explicit']

    def test_expected_values(self, content_restrictions: ContentRestrictions) -> None:
        assert content_restrictions.available == self.available
        assert content_restrictions.disclaimers == self.disclaimers

    def test_de_json_none(self, client: Client) -> None:
        assert ContentRestrictions.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'available': self.available,
            'disclaimers': self.disclaimers,
        }
        content_restrictions = ContentRestrictions.de_json(json_dict, client)
        assert content_restrictions is not None

        assert content_restrictions.available == self.available
        assert content_restrictions.disclaimers == self.disclaimers

    def test_equality(self) -> None:
        a = ContentRestrictions(available=self.available, disclaimers=self.disclaimers)
        b = ContentRestrictions(available=False, disclaimers=[])
        c = ContentRestrictions(available=self.available, disclaimers=self.disclaimers)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
