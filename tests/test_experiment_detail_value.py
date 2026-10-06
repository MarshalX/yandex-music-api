from typing import Dict

from yandex_music import Client, ExperimentDetailValue, JSONType


class TestExperimentDetailValue:
    title = 'test_group'
    enabled = True
    delay = 42

    def test_expected_values(self, experiment_detail_value: ExperimentDetailValue) -> None:
        assert experiment_detail_value.title == self.title
        assert experiment_detail_value.__dict__['enabled'] == self.enabled
        assert experiment_detail_value.__dict__['delay'] == self.delay

    def test_de_json_none(self, client: Client) -> None:
        assert ExperimentDetailValue.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'title': self.title}
        value = ExperimentDetailValue.de_json(json_dict, client)
        assert value is not None

        assert value.title == self.title

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'enabled': self.enabled,
            'delay': self.delay,
            'trackSkipTimeoutSec': 15,
        }
        value = ExperimentDetailValue.de_json(json_dict, client)
        assert value is not None

        assert value.title == self.title
        assert value.__dict__['enabled'] == self.enabled
        assert value.__dict__['delay'] == self.delay
        # camelCase ключ нормализуется в snake_case
        assert value.__dict__['track_skip_timeout_sec'] == 15

    def test_de_json_title_non_string(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'title': 123}
        value = ExperimentDetailValue.de_json(json_dict, client)
        assert value is not None

        assert value.title is None

    def test_equality(self) -> None:
        a = ExperimentDetailValue(title=self.title)
        b = ExperimentDetailValue(title='other_group')
        c = ExperimentDetailValue(title=self.title)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
