from typing import Dict

from yandex_music import CaseForms, Client, JSONType, MadeFor, User


class TestMadeFor:
    def test_expected_values(self, made_for: MadeFor, user: User, case_forms: CaseForms) -> None:
        assert made_for.user_info == user
        assert made_for.case_forms == case_forms

    def test_de_json_none(self, client: Client) -> None:
        assert MadeFor.de_json({}, client) is None

    def test_de_json_required(self, user: User) -> None:
        json_dict: Dict[str, JSONType] = {'user_info': user.to_dict()}
        made_for = MadeFor.de_json(json_dict, Client(strict=True))
        assert made_for is not None

        assert made_for.user_info == user
        assert made_for.case_forms is None

    def test_de_json_all(self, client: Client, user: User, case_forms: CaseForms) -> None:
        json_dict: Dict[str, JSONType] = {'user_info': user.to_dict(), 'case_forms': case_forms.to_dict()}
        made_for = MadeFor.de_json(json_dict, client)
        assert made_for is not None

        assert made_for.user_info == user
        assert made_for.case_forms == case_forms

    def test_equality(self, user: User, case_forms: CaseForms) -> None:
        a = MadeFor(user_info=user, case_forms=case_forms)

        assert a != user
        assert a != case_forms
        assert hash(a) != hash(user) != hash(case_forms)
