from yandex_music import ExperimentDetailValue


class TestExperimentDetailValue:
    title = 'test_group'
    enabled = True
    delay = 42

    def test_expected_values(self, experiment_detail_value):
        assert experiment_detail_value.title == self.title
        assert experiment_detail_value.enabled == self.enabled
        assert experiment_detail_value.delay == self.delay

    def test_de_json_none(self, client):
        assert ExperimentDetailValue.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'title': self.title}
        value = ExperimentDetailValue.de_json(json_dict, client)

        assert value.title == self.title

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'enabled': self.enabled,
            'delay': self.delay,
            'trackSkipTimeoutSec': 15,
        }
        value = ExperimentDetailValue.de_json(json_dict, client)

        assert value.title == self.title
        assert value.enabled == self.enabled
        assert value.delay == self.delay
        # camelCase ключ нормализуется в snake_case
        assert value.track_skip_timeout_sec == 15

    def test_de_json_title_non_string(self, client):
        json_dict = {'title': 123}
        value = ExperimentDetailValue.de_json(json_dict, client)

        assert value.title is None

    def test_equality(self):
        a = ExperimentDetailValue(title=self.title)
        b = ExperimentDetailValue(title='other_group')
        c = ExperimentDetailValue(title=self.title)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
