from yandex_music import ExperimentsDetails


class TestExperimentsDetails:
    def test_expected_values(self, experiments_details, experiment_detail):
        assert experiments_details.experiments == {'TestExperiment': experiment_detail}

    def test_de_json_none(self, client):
        assert ExperimentsDetails.de_json({}, client) is None

    def test_de_json_all(self, client, experiment_detail):
        json_dict = {'TestExperiment': experiment_detail.to_dict()}
        details = ExperimentsDetails.de_json(json_dict, client)

        assert 'TestExperiment' in details.experiments
        assert details.experiments['TestExperiment'] == experiment_detail

    def test_de_json_preserves_original_keys(self, client, experiment_detail):
        # Ключи экспериментов сохраняются как есть (CamelCase, с цифрами и т. п.)
        json_dict = {
            'AliceTest': experiment_detail.to_dict(),
            '3dsRubilnik': experiment_detail.to_dict(),
        }
        details = ExperimentsDetails.de_json(json_dict, client)

        assert set(details.experiments.keys()) == {'AliceTest', '3dsRubilnik'}

    def test_de_json_skips_non_dict_entries(self, client, experiment_detail):
        json_dict = {'Good': experiment_detail.to_dict(), 'Bad': 'not-a-dict'}
        details = ExperimentsDetails.de_json(json_dict, client)

        assert 'Good' in details.experiments
        assert 'Bad' not in details.experiments
