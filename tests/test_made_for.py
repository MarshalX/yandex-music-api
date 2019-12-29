from yandex_music import MadeFor


class TestMadeFor:
    def test_expected_values(self, made_for, user, case_forms):
        assert made_for.user_info == user
        assert made_for.case_forms == case_forms

    def test_de_json_none(self, client):
        assert MadeFor.de_json({}, client) is None

    def test_de_json_required(self, client, user, case_forms):
        json_dict = {'user_info': user.to_dict(), 'case_forms': case_forms.to_dict()}
        made_for = MadeFor.de_json(json_dict, client)

        assert made_for.user_info == user
        assert made_for.case_forms == case_forms

    def test_de_json_all(self, client, user, case_forms):
        json_dict = {'user_info': user.to_dict(), 'case_forms': case_forms.to_dict()}
        made_for = MadeFor.de_json(json_dict, client)

        assert made_for.user_info == user
        assert made_for.case_forms == case_forms

    def test_equality(self, user, case_forms):
        a = MadeFor(user, case_forms)

        assert a != user and a != case_forms
        assert hash(a) != hash(user) != hash(case_forms)
