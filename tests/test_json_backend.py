import importlib
import json
import subprocess
import sys
from typing import Callable, Dict, Iterator, List, Union
from unittest.mock import MagicMock, patch

import pytest

from yandex_music import Client, ClientAsync, Icon, JSONType
from yandex_music.utils import json_backend
from yandex_music.utils.difference import Difference
from yandex_music.utils.json_backend import (
    JsonBackend,
    OrjsonBackend,
    PydanticCoreBackend,
    StdlibBackend,
    UjsonBackend,
    detect_json_backend,
    get_default_json_backend,
    set_default_json_backend,
)
from yandex_music.utils.request import Request
from yandex_music.utils.request_base import USER_AGENT, RequestBase, default_timeout

BACKEND_FACTORIES: Dict[str, Callable[[], JsonBackend]] = {
    'stdlib': StdlibBackend,
    'orjson': OrjsonBackend,
    'pydantic_core': PydanticCoreBackend,
    'ujson': UjsonBackend,
}

TEST_DATA: List[JSONType] = [
    {'simple': 'dict'},
    {'nested': {'key': [1, 2, 3]}},
    {'unicode': 'кириллица'},
    [1, 'two', 3.5, True, None],
    {'empty_list': [], 'empty_dict': {}},
]


class RecordingBackend:
    def __init__(self) -> None:
        self._inner = StdlibBackend()
        self.loads_calls = 0
        self.dumps_calls = 0

    def loads(self, data: Union[bytes, str]) -> object:
        self.loads_calls += 1
        return self._inner.loads(data)

    def dumps(self, obj: object) -> str:
        self.dumps_calls += 1
        return self._inner.dumps(obj)


@pytest.fixture(autouse=True)
def _reset_json_backend() -> Iterator[None]:
    yield
    set_default_json_backend(None)
    json_backend._detected_backend = None


@pytest.fixture(params=list(BACKEND_FACTORIES))
def backend(request: pytest.FixtureRequest) -> JsonBackend:
    name: str = request.param
    try:
        return BACKEND_FACTORIES[name]()
    except ImportError:
        pytest.skip(f'{name} not installed')


class TestBackends:
    def test_loads_bytes(self, backend: JsonBackend) -> None:
        assert backend.loads(b'{"key": "value"}') == {'key': 'value'}

    def test_loads_str(self, backend: JsonBackend) -> None:
        assert backend.loads('{"key": "value"}') == {'key': 'value'}

    def test_loads_unicode_bytes(self, backend: JsonBackend) -> None:
        assert backend.loads('{"key": "значение"}'.encode()) == {'key': 'значение'}

    def test_dumps_returns_str(self, backend: JsonBackend) -> None:
        assert isinstance(backend.dumps({'key': 'value'}), str)

    def test_dumps_unicode_not_escaped(self, backend: JsonBackend) -> None:
        result = backend.dumps({'key': 'значение'})
        assert 'значение' in result
        assert '\\u' not in result

    @pytest.mark.parametrize('data', TEST_DATA)
    def test_roundtrip(self, backend: JsonBackend, data: JSONType) -> None:
        assert backend.loads(backend.dumps(data)) == data

    @pytest.mark.parametrize('data', TEST_DATA)
    def test_loads_stdlib_output(self, backend: JsonBackend, data: JSONType) -> None:
        assert backend.loads(json.dumps(data)) == data

    def test_loads_invalid_raises_value_error(self, backend: JsonBackend) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            _ = backend.loads(b'not json')


class TestDetect:
    @pytest.mark.parametrize(
        ('missing', 'expected'),
        [
            ([], OrjsonBackend),
            (['orjson'], PydanticCoreBackend),
            (['orjson', 'pydantic_core'], UjsonBackend),
            (['orjson', 'pydantic_core', 'ujson'], StdlibBackend),
        ],
    )
    def test_priority(self, missing: List[str], expected: type) -> None:
        for name in ('orjson', 'pydantic_core', 'ujson'):
            if name not in missing:
                _ = pytest.importorskip(name)

        with patch.dict(sys.modules, dict.fromkeys(missing)):
            json_backend._detected_backend = None
            assert isinstance(detect_json_backend(), expected)

    def test_cached(self) -> None:
        assert detect_json_backend() is detect_json_backend()


class TestDefault:
    def test_default_is_detected(self) -> None:
        assert get_default_json_backend() is detect_json_backend()

    def test_set_and_reset(self) -> None:
        custom = RecordingBackend()
        set_default_json_backend(custom)
        assert get_default_json_backend() is custom

        set_default_json_backend(None)
        assert get_default_json_backend() is detect_json_backend()

    def test_json_compat_deprecated(self) -> None:
        with pytest.warns(DeprecationWarning, match='json_backend'):
            _ = importlib.reload(importlib.import_module('yandex_music.utils.json_compat'))

    def test_json_compat_uses_default(self) -> None:
        with pytest.warns(DeprecationWarning, match='json_backend'):
            json_compat = importlib.reload(importlib.import_module('yandex_music.utils.json_compat'))
        custom = RecordingBackend()
        set_default_json_backend(custom)

        assert json_compat.loads(json_compat.dumps({'a': 1})) == {'a': 1}
        assert custom.dumps_calls == 1
        assert custom.loads_calls == 1


class TestRequest:
    def test_default_follows_global(self) -> None:
        req = RequestBase()
        custom = RecordingBackend()
        set_default_json_backend(custom)
        assert req.json_backend is custom

    def test_explicit_overrides_global(self) -> None:
        explicit = RecordingBackend()
        req = RequestBase(json_backend=explicit)
        set_default_json_backend(RecordingBackend())
        assert req.json_backend is explicit

    def test_parse_uses_backend(self) -> None:
        explicit = RecordingBackend()
        req = RequestBase(json_backend=explicit)
        req.client = MagicMock()

        response = req._parse(b'{"result": {"key": "value"}}')

        assert response is not None
        assert response.get_result() == {'key': 'value'}
        assert explicit.loads_calls == 1

    def test_json_body_serialized_by_backend(self) -> None:
        explicit = RecordingBackend()
        req = RequestBase(json_backend=explicit)
        shared_headers = {'X-Test': '1'}

        kwargs = req._prepare_kwargs(
            {'headers': shared_headers, 'json': {'key': 'значение'}, 'timeout': default_timeout}
        )

        assert 'json' not in kwargs
        assert kwargs['data'] == '{"key": "значение"}'.encode()
        assert kwargs['headers'] == {'X-Test': '1', 'User-Agent': USER_AGENT, 'Content-Type': 'application/json'}
        assert 'Content-Type' not in shared_headers
        assert explicit.dumps_calls == 1

    def test_without_json_body_data_untouched(self) -> None:
        req = RequestBase(json_backend=RecordingBackend())
        kwargs = req._prepare_kwargs({'data': {'a': '1'}, 'timeout': default_timeout})
        assert kwargs['data'] == {'a': '1'}
        assert kwargs['headers'] == {'User-Agent': USER_AGENT}

    def test_json_and_data_conflict(self) -> None:
        req = RequestBase()
        with pytest.raises(ValueError, match='data and json'):
            _ = req._prepare_kwargs({'data': 'x', 'json': {'a': 1}, 'timeout': default_timeout})


class TestClient:
    def test_client_param(self) -> None:
        explicit = RecordingBackend()
        client = Client(json_backend=explicit)
        assert client.request.json_backend is explicit

    def test_client_param_overrides_request(self) -> None:
        explicit = RecordingBackend()
        client = Client(request=Request(json_backend=RecordingBackend()), json_backend=explicit)
        assert client.request.json_backend is explicit

    def test_request_backend_kept(self) -> None:
        explicit = RecordingBackend()
        client = Client(request=Request(json_backend=explicit))
        assert client.request.json_backend is explicit

    def test_async_client_param(self) -> None:
        explicit = RecordingBackend()
        client = ClientAsync(json_backend=explicit)
        assert client.request.json_backend is explicit

    def test_model_to_json_uses_client_backend(self) -> None:
        explicit = RecordingBackend()
        icon = Icon(background_color='#fff', image_url='url', client=Client(json_backend=explicit))

        assert json.loads(icon.to_json()) == {'background_color': '#fff', 'image_url': 'url'}
        assert explicit.dumps_calls == 1

    def test_model_to_json_without_client_uses_default(self) -> None:
        custom = RecordingBackend()
        set_default_json_backend(custom)

        _ = Icon(background_color='#fff', image_url='url').to_json()

        assert custom.dumps_calls == 1


class TestDifference:
    def test_explicit_backend(self) -> None:
        explicit = RecordingBackend()
        diff = Difference().add_delete(0, 1)

        assert json.loads(diff.to_json(explicit)) == [{'op': 'delete', 'from': 0, 'to': 1}]
        assert explicit.dumps_calls == 1

    def test_default_backend(self) -> None:
        custom = RecordingBackend()
        set_default_json_backend(custom)

        _ = Difference().add_delete(0, 1).to_json()

        assert custom.dumps_calls == 1


class TestYnison:
    @pytest.fixture(autouse=True)
    def _require_ynison(self) -> None:
        _ = pytest.importorskip('betterproto')
        _ = pytest.importorskip('websockets')

    def test_dump_request_matches_betterproto(self) -> None:
        from yandex_music.ynison.client import YnisonClient

        client = YnisonClient('fake-token', device_id='810eb13dbcd1', json_backend=StdlibBackend())
        request = client._full_state_request()

        assert json.loads(client._dump_request(request)) == json.loads(request.to_json())

    def test_explicit_backend_used(self) -> None:
        from yandex_music.ynison.client_async import YnisonClientAsync

        explicit = RecordingBackend()
        client = YnisonClientAsync('fake-token', device_id='810eb13dbcd1', json_backend=explicit)
        set_default_json_backend(RecordingBackend())

        _ = client._get_subprotocols()
        _ = client._parse_redirect_frame(
            json.dumps({'host': 'example.invalid', 'redirectTicket': 'ticket', 'sessionId': '1'})
        )

        assert explicit.dumps_calls == 2
        assert explicit.loads_calls == 1
