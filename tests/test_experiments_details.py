from typing import Dict

from yandex_music import Client, ExperimentDetail, ExperimentsDetails, JSONType


class TestExperimentsDetails:
    def test_expected_values(
        self, experiments_details: ExperimentsDetails, experiment_detail: ExperimentDetail
    ) -> None:
        assert experiments_details.experiments == {'TestExperiment': experiment_detail}

    def test_de_json_none(self, client: Client) -> None:
        assert ExperimentsDetails.de_json({}, client) is None

    def test_de_json_all(self, client: Client, experiment_detail: ExperimentDetail) -> None:
        json_dict: Dict[str, JSONType] = {'TestExperiment': experiment_detail.to_dict()}
        details = ExperimentsDetails.de_json(json_dict, client)
        assert details is not None

        assert 'TestExperiment' in details.experiments
        assert details.experiments['TestExperiment'] == experiment_detail

    def test_de_json_preserves_original_keys(self, client: Client, experiment_detail: ExperimentDetail) -> None:
        # Ключи экспериментов сохраняются как есть (CamelCase, с цифрами и т. п.)
        json_dict: Dict[str, JSONType] = {
            'AliceTest': experiment_detail.to_dict(),
            '3dsRubilnik': experiment_detail.to_dict(),
        }
        details = ExperimentsDetails.de_json(json_dict, client)
        assert details is not None

        assert set(details.experiments.keys()) == {'AliceTest', '3dsRubilnik'}

    def test_de_json_skips_non_dict_entries(self, client: Client, experiment_detail: ExperimentDetail) -> None:
        json_dict: Dict[str, JSONType] = {'Good': experiment_detail.to_dict(), 'Bad': 'not-a-dict'}
        details = ExperimentsDetails.de_json(json_dict, client)
        assert details is not None

        assert 'Good' in details.experiments
        assert 'Bad' not in details.experiments
