from typing import Dict

from yandex_music import Client, ExperimentDetail, ExperimentDetailValue, JSONType


class TestExperimentDetail:
    group = 'test_group'

    def test_expected_values(
        self, experiment_detail: ExperimentDetail, experiment_detail_value: ExperimentDetailValue
    ) -> None:
        assert experiment_detail.group == self.group
        assert experiment_detail.value == experiment_detail_value

    def test_de_json_none(self, client: Client) -> None:
        assert ExperimentDetail.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'group': self.group}
        detail = ExperimentDetail.de_json(json_dict, client)
        assert detail is not None

        assert detail.group == self.group
        assert detail.value is None

    def test_de_json_all(self, client: Client, experiment_detail_value: ExperimentDetailValue) -> None:
        json_dict: Dict[str, JSONType] = {'group': self.group, 'value': experiment_detail_value.to_dict()}
        detail = ExperimentDetail.de_json(json_dict, client)
        assert detail is not None

        assert detail.group == self.group
        assert detail.value == experiment_detail_value

    def test_equality(self, experiment_detail_value: ExperimentDetailValue) -> None:
        a = ExperimentDetail(group=self.group, value=experiment_detail_value)
        b = ExperimentDetail(group='other_group', value=experiment_detail_value)
        c = ExperimentDetail(group=self.group, value=experiment_detail_value)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
