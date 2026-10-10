from typing import Dict

from yandex_music import CaseForms, Client, JSONType, MadeForUser


class TestMadeForUser:
    is_made_for_user = True

    def test_expected_values(self, made_for_user: MadeForUser, case_forms: CaseForms) -> None:
        assert made_for_user.is_made_for_user == self.is_made_for_user
        assert made_for_user.case_forms == case_forms

    def test_de_json_none(self, client: Client) -> None:
        assert MadeForUser.de_json({}, client) is None

    def test_de_json_all(self, client: Client, case_forms: CaseForms) -> None:
        json_dict: Dict[str, JSONType] = {
            'isMadeForUser': self.is_made_for_user,
            'caseForms': case_forms.to_dict(),
        }
        obj = MadeForUser.de_json(json_dict, client)
        assert obj is not None

        assert obj.is_made_for_user == self.is_made_for_user
        assert obj.case_forms == case_forms

    def test_equality(self, case_forms: CaseForms) -> None:
        a = MadeForUser(is_made_for_user=True, case_forms=case_forms)
        b = MadeForUser(is_made_for_user=False, case_forms=case_forms)
        c = MadeForUser(is_made_for_user=True, case_forms=case_forms)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
