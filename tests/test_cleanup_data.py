from dataclasses import field
from typing import Dict, Optional, Tuple
from unittest.mock import MagicMock

import pytest

from yandex_music.base import JSONType, YandexMusicModel
from yandex_music.utils import model


@model
class SampleModel(YandexMusicModel):
    client: Optional[object] = field(default=None, repr=False)
    name: Optional[str] = None
    value: Optional[int] = None


class TestCleanupData:
    def test_returns_empty_dict_for_none(self) -> None:
        assert SampleModel.cleanup_data(None, None) == {}

    def test_returns_empty_dict_for_empty_dict(self) -> None:
        assert SampleModel.cleanup_data({}, None) == {}

    def test_returns_empty_dict_for_non_dict(self) -> None:
        assert SampleModel.cleanup_data([1, 2, 3], None) == {}
        assert SampleModel.cleanup_data('string', None) == {}
        assert SampleModel.cleanup_data(42, None) == {}

    def test_keeps_known_fields(self) -> None:
        data: Dict[str, JSONType] = {'name': 'test', 'value': 42, 'client': None}
        result = SampleModel.cleanup_data(data, None)
        assert result == {'name': 'test', 'value': 42, 'client': None}

    def test_strips_unknown_fields(self) -> None:
        data: Dict[str, JSONType] = {'name': 'test', 'unknown_field': 'drop_me', 'another': 123}
        result = SampleModel.cleanup_data(data, None)
        assert result == {'name': 'test'}

    def test_does_not_mutate_input(self) -> None:
        data: Dict[str, JSONType] = {'name': 'test', 'extra': 'value'}
        original = data.copy()
        _ = SampleModel.cleanup_data(data, None)
        assert data == original

    def test_all_unknown_fields(self) -> None:
        data: Dict[str, JSONType] = {'foo': 1, 'bar': 2}
        result = SampleModel.cleanup_data(data, None)
        assert result == {}

    def test_report_unknown_fields_callback(self) -> None:
        client = MagicMock()
        client.report_unknown_fields = True

        with pytest.MonkeyPatch.context() as mp:
            callback = MagicMock()
            mp.setattr(SampleModel, 'report_unknown_fields_callback', callback)

            _ = SampleModel.cleanup_data({'name': 'test', 'unknown': 1, 'extra': 2}, client)

            callback.assert_called_once()
            args: Tuple[object, ...] = callback.call_args[0]
            assert args[0] is SampleModel
            assert args[1] == {'extra', 'unknown'}

    def test_no_report_when_disabled(self) -> None:
        client = MagicMock()
        client.report_unknown_fields = False

        with pytest.MonkeyPatch.context() as mp:
            callback = MagicMock()
            mp.setattr(SampleModel, 'report_unknown_fields_callback', callback)

            _ = SampleModel.cleanup_data({'name': 'test', 'unknown': 1}, client)
            callback.assert_not_called()

    def test_no_report_when_no_unknown(self) -> None:
        client = MagicMock()
        client.report_unknown_fields = True

        with pytest.MonkeyPatch.context() as mp:
            callback = MagicMock()
            mp.setattr(SampleModel, 'report_unknown_fields_callback', callback)

            _ = SampleModel.cleanup_data({'name': 'test', 'value': 1}, client)
            callback.assert_not_called()

    def test_normalizes_camel_case_keys(self) -> None:
        data: Dict[str, JSONType] = {'Name': 'test', 'Value': 42}
        result = SampleModel.cleanup_data(data, None)
        assert result == {'name': 'test', 'value': 42}

    def test_normalizes_camel_case_and_strips_unknown(self) -> None:
        data: Dict[str, JSONType] = {'name': 'test', 'unknownField': 'drop_me', 'anotherThing': 123}
        result = SampleModel.cleanup_data(data, None)
        assert result == {'name': 'test'}

    def test_de_json_integration(self) -> None:
        client = MagicMock()
        client.report_unknown_fields = False

        obj = SampleModel.de_json({'name': 'hello', 'value': 5, 'junk': 'ignored'}, client)
        assert obj is not None
        assert obj.name == 'hello'
        assert obj.value == 5
        assert not hasattr(obj, 'junk')

    def test_de_json_with_camel_case(self) -> None:
        client = MagicMock()
        client.report_unknown_fields = False

        obj = SampleModel.de_json({'Name': 'hello', 'Value': 5}, client)
        assert obj is not None
        assert obj.name == 'hello'
        assert obj.value == 5
