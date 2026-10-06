from typing import Dict

from yandex_music import Client, CombinedSessionItem, CombinedSessionLanding, JSONType


class TestCombinedSessionLanding:
    title = 'Время клипов'
    description = 'Персональная подборка клипов'
    button = 'Смотреть'

    def test_expected_values(
        self, combined_session_landing: CombinedSessionLanding, combined_session_item: CombinedSessionItem
    ) -> None:
        assert combined_session_landing.title == self.title
        assert combined_session_landing.description == self.description
        assert combined_session_landing.button == self.button
        assert combined_session_landing.list == [combined_session_item]

    def test_de_json_none(self, client: Client) -> None:
        assert CombinedSessionLanding.de_json({}, client) is None

    def test_de_json_all(self, client: Client, combined_session_item: CombinedSessionItem) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'description': self.description,
            'button': self.button,
            'list': [combined_session_item.to_dict()],
        }
        combined_session_landing = CombinedSessionLanding.de_json(json_dict, client)
        assert combined_session_landing is not None

        assert combined_session_landing.title == self.title
        assert combined_session_landing.description == self.description
        assert combined_session_landing.button == self.button
        assert combined_session_landing.list == [combined_session_item]

    def test_equality(self, combined_session_item: CombinedSessionItem) -> None:
        a = CombinedSessionLanding(self.title, list=[combined_session_item])
        b = CombinedSessionLanding('Other', list=[combined_session_item])
        c = CombinedSessionLanding(self.title, list=[combined_session_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
