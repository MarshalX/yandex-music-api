from yandex_music import ExperimentDetail


class TestExperimentDetail:
    group = 'test_group'

    def test_expected_values(self, experiment_detail, experiment_detail_value):
        assert experiment_detail.group == self.group
        assert experiment_detail.value == experiment_detail_value

    def test_de_json_none(self, client):
        assert ExperimentDetail.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'group': self.group}
        detail = ExperimentDetail.de_json(json_dict, client)

        assert detail.group == self.group
        assert detail.value is None

    def test_de_json_all(self, client, experiment_detail_value):
        json_dict = {'group': self.group, 'value': experiment_detail_value.to_dict()}
        detail = ExperimentDetail.de_json(json_dict, client)

        assert detail.group == self.group
        assert detail.value == experiment_detail_value

    def test_equality(self, experiment_detail_value):
        a = ExperimentDetail(group=self.group, value=experiment_detail_value)
        b = ExperimentDetail(group='other_group', value=experiment_detail_value)
        c = ExperimentDetail(group=self.group, value=experiment_detail_value)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
