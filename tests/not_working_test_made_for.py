from yandex_music import MadeFor


class TestMadeFor:

    def test_expected_values(self, made_for, user_info, case_forms):
        assert made_for.user_info == user_info
        assert made_for.case_forms == case_forms

    def test_de_json_required(self, client, user_info, case_forms):
        json_dict = {'user_info': user_info, 'case_forms': case_forms}
        made_for = MadeFor.de_json(json_dict, client)

        assert made_for.user_info == user_info
        assert made_for.case_forms == case_forms

    def test_de_json_all(self, client, user_info, case_forms):
        json_dict = {'user_info': user_info, 'case_forms': case_forms}
        made_for = MadeFor.de_json(json_dict, client)

        assert made_for.user_info == user_info
        assert made_for.case_forms == case_forms

    def test_equality(self):
        pass
