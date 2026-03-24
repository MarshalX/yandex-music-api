import importlib
import json
import sys
from unittest.mock import patch

import pytest

from yandex_music.utils import json_compat


class TestWithOrjson:
    """Тесты json_compat при наличии orjson."""

    @pytest.fixture(autouse=True)
    def _reload_with_orjson(self):
        """Перезагрузка модуля с orjson."""
        importlib.reload(json_compat)
        if not json_compat.accepts_bytes:
            pytest.skip('orjson not installed')

    def test_accepts_bytes_true(self):
        assert json_compat.accepts_bytes is True

    def test_loads_bytes(self):
        result = json_compat.loads(b'{"key": "value"}')
        assert result == {'key': 'value'}

    def test_loads_str(self):
        result = json_compat.loads('{"key": "value"}')
        assert result == {'key': 'value'}

    def test_loads_nested(self):
        data = b'{"a": {"b": [1, 2, 3]}}'
        result = json_compat.loads(data)
        assert result == {'a': {'b': [1, 2, 3]}}

    def test_loads_unicode(self):
        result = json_compat.loads('{"key": "значение"}'.encode('UTF-8'))
        assert result == {'key': 'значение'}

    def test_dumps_returns_str(self):
        result = json_compat.dumps({'key': 'value'})
        assert isinstance(result, str)

    def test_dumps_unicode_not_escaped(self):
        result = json_compat.dumps({'key': 'значение'})
        assert 'значение' in result
        assert '\\u' not in result

    def test_dumps_roundtrip(self):
        original = {'a': 1, 'b': [2, 3], 'c': 'text'}
        result = json_compat.loads(json_compat.dumps(original))
        assert result == original

    def test_loads_invalid_json(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            json_compat.loads(b'not json')


class TestWithoutOrjson:
    """Тесты json_compat при отсутствии orjson (stdlib json fallback)."""

    @pytest.fixture(autouse=True)
    def _reload_without_orjson(self):
        """Перезагрузка модуля без orjson."""
        with patch.dict(sys.modules, {'orjson': None}):
            importlib.reload(json_compat)
            yield
        importlib.reload(json_compat)

    def test_accepts_bytes_false(self):
        assert json_compat.accepts_bytes is False

    def test_loads_bytes(self):
        result = json_compat.loads(b'{"key": "value"}')
        assert result == {'key': 'value'}

    def test_loads_str(self):
        result = json_compat.loads('{"key": "value"}')
        assert result == {'key': 'value'}

    def test_loads_nested(self):
        data = b'{"a": {"b": [1, 2, 3]}}'
        result = json_compat.loads(data)
        assert result == {'a': {'b': [1, 2, 3]}}

    def test_loads_unicode(self):
        result = json_compat.loads('{"key": "значение"}'.encode('UTF-8'))
        assert result == {'key': 'значение'}

    def test_dumps_returns_str(self):
        result = json_compat.dumps({'key': 'value'})
        assert isinstance(result, str)

    def test_dumps_unicode_not_escaped(self):
        result = json_compat.dumps({'key': 'значение'})
        assert 'значение' in result
        assert '\\u' not in result

    def test_dumps_roundtrip(self):
        original = {'a': 1, 'b': [2, 3], 'c': 'text'}
        result = json_compat.loads(json_compat.dumps(original))
        assert result == original

    def test_loads_invalid_json(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            json_compat.loads(b'not json')

    def test_loads_invalid_utf8(self):
        with pytest.raises(UnicodeDecodeError):
            json_compat.loads(b'\xff\xfe')


class TestConsistency:
    """Оба бэкенда должны давать одинаковый результат."""

    TEST_DATA = [
        {'simple': 'dict'},
        {'nested': {'key': [1, 2, 3]}},
        {'unicode': 'кириллица'},
        [1, 'two', 3.0, True, None],
        {'empty_list': [], 'empty_dict': {}},
    ]

    @pytest.mark.parametrize('data', TEST_DATA)
    def test_dumps_loads_roundtrip(self, data):
        serialized = json_compat.dumps(data)
        assert isinstance(serialized, str)
        deserialized = json_compat.loads(serialized)
        assert deserialized == data

    @pytest.mark.parametrize('data', TEST_DATA)
    def test_loads_from_stdlib_json(self, data):
        """json_compat.loads should parse stdlib json.dumps output."""
        stdlib_json = json.dumps(data, ensure_ascii=False)
        result = json_compat.loads(stdlib_json)
        assert result == data

    @pytest.mark.parametrize('data', TEST_DATA)
    def test_loads_bytes_from_stdlib_json(self, data):
        """json_compat.loads should parse stdlib json.dumps output as bytes."""
        stdlib_bytes = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        result = json_compat.loads(stdlib_bytes)
        assert result == data
