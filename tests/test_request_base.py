import json
from unittest.mock import MagicMock

import pytest

from yandex_music.exceptions import (
    BadRequestError,
    NetworkError,
    NotFoundError,
    UnauthorizedError,
    YandexMusicError,
)
from yandex_music.utils.normalize import _convert_camel_to_snake, _normalize_key
from yandex_music.utils.request_base import (
    DEFAULT_TIMEOUT,
    HEADERS,
    USER_AGENT,
    RequestBase,
    default_timeout,
)


class TestConvertCamelToSnake:
    @pytest.mark.parametrize(
        'input_, expected',
        [
            ('camelCase', 'camel_case'),
            ('CamelCase', 'camel_case'),
            ('getHTTPResponse', 'get_http_response'),
            ('HTMLParser', 'html_parser'),
            ('simpleXMLParser', 'simple_xml_parser'),
            ('already_snake', 'already_snake'),
            ('lowercase', 'lowercase'),
            ('ALLCAPS', 'allcaps'),
            ('a', 'a'),
            ('AB', 'ab'),
            ('getURL', 'get_url'),
            ('iPhone', 'i_phone'),
            ('test123Value', 'test123_value'),
            ('value2X', 'value2_x'),
        ],
    )
    def test_conversion(self, input_, expected):
        assert _convert_camel_to_snake(input_) == expected

    def test_caching(self):
        _convert_camel_to_snake.cache_clear()
        _convert_camel_to_snake('testCaching')
        _convert_camel_to_snake('testCaching')
        info = _convert_camel_to_snake.cache_info()
        assert info.hits >= 1


class TestNormalizeKey:
    @pytest.mark.parametrize(
        'input_, expected',
        [
            ('camelCase', 'camel_case'),
            ('some-key', 'some_key'),
            ('kebab-Case', 'kebab__case'),
            ('a-b-c', 'a_b_c'),
        ],
    )
    def test_basic(self, input_, expected):
        assert _normalize_key(input_) == expected

    @pytest.mark.parametrize('word', ['class', 'return', 'import', 'for', 'if', 'while', 'lambda'])
    def test_reserved_words(self, word):
        assert _normalize_key(word) == word + '_'

    def test_client_type_not_reserved_after_snake(self):
        # 'ClientType' is in reserved_names but after snake conversion becomes 'client_type'
        # which is NOT in the reserved set, so no suffix is added
        assert _normalize_key('ClientType') == 'client_type'

    @pytest.mark.parametrize(
        'input_, expected',
        [
            ('1bad', '_1bad'),
            ('2things', '_2things'),
            ('0x', '_0x'),
        ],
    )
    def test_digit_prefix(self, input_, expected):
        assert _normalize_key(input_) == expected

    def test_empty_string(self):
        assert _normalize_key('') == ''

    def test_caching(self):
        _normalize_key.cache_clear()
        _normalize_key('cachingTestKey')
        _normalize_key('cachingTestKey')
        info = _normalize_key.cache_info()
        assert info.hits >= 1


class TestRequestBaseInit:
    def test_default_headers(self):
        req = RequestBase()
        assert req.headers == HEADERS
        assert req.headers is not HEADERS

    def test_custom_headers(self):
        custom = {'X-Custom': 'value'}
        req = RequestBase(headers=custom)
        assert req.headers == custom

    def test_default_timeout(self):
        req = RequestBase()
        assert req._timeout == DEFAULT_TIMEOUT

    def test_custom_timeout(self):
        req = RequestBase(timeout=10)
        assert req._timeout == 10

    def test_proxy_url(self):
        req = RequestBase(proxy_url='http://proxy:8080')
        assert req.proxy_url == 'http://proxy:8080'
        assert req.proxies == {'http': 'http://proxy:8080', 'https': 'http://proxy:8080'}

    def test_no_proxy(self):
        req = RequestBase()
        assert req.proxy_url is None
        assert req.proxies is None


class TestSetters:
    def test_set_language(self):
        req = RequestBase()
        req.set_language('ru')
        assert req.headers['Accept-Language'] == 'ru'

    def test_set_timeout_custom(self):
        req = RequestBase()
        req.set_timeout(30)
        assert req._timeout == 30

    def test_set_timeout_default(self):
        req = RequestBase(timeout=30)
        req.set_timeout(default_timeout)
        assert req._timeout == DEFAULT_TIMEOUT

    def test_set_authorization(self):
        req = RequestBase()
        req.set_authorization('my_token')
        assert req.headers['Authorization'] == 'OAuth my_token'


class TestSetAndReturnClient:
    def test_sets_client(self):
        req = RequestBase()
        mock_client = MagicMock()
        mock_client.token = None
        result = req.set_and_return_client(mock_client)
        assert req.client is mock_client
        assert result is mock_client

    def test_sets_authorization_when_token_present(self):
        req = RequestBase()
        mock_client = MagicMock()
        mock_client.token = 'test_token'
        req.set_and_return_client(mock_client)
        assert req.headers['Authorization'] == 'OAuth test_token'

    def test_no_authorization_when_no_token(self):
        req = RequestBase()
        mock_client = MagicMock()
        mock_client.token = None
        req.set_and_return_client(mock_client)
        assert 'Authorization' not in req.headers


class TestPrepareKwargs:
    def test_adds_user_agent(self):
        req = RequestBase()
        kwargs = {'timeout': 5, 'headers': {}}
        result = req._prepare_kwargs(kwargs)
        assert result['headers']['User-Agent'] == USER_AGENT

    def test_creates_headers_if_missing(self):
        req = RequestBase()
        kwargs = {'timeout': 5}
        result = req._prepare_kwargs(kwargs)
        assert 'headers' in result
        assert result['headers']['User-Agent'] == USER_AGENT

    def test_preserves_existing_headers(self):
        req = RequestBase()
        kwargs = {'timeout': 5, 'headers': {'X-Custom': 'value'}}
        result = req._prepare_kwargs(kwargs)
        assert result['headers']['X-Custom'] == 'value'
        assert result['headers']['User-Agent'] == USER_AGENT

    def test_resolves_default_timeout(self):
        req = RequestBase(timeout=15)
        kwargs = {'timeout': default_timeout}
        result = req._prepare_kwargs(kwargs)
        assert result['timeout'] == 15

    def test_keeps_explicit_timeout(self):
        req = RequestBase(timeout=15)
        kwargs = {'timeout': 30}
        result = req._prepare_kwargs(kwargs)
        assert result['timeout'] == 30

    def test_mutates_in_place(self):
        req = RequestBase()
        kwargs = {'timeout': 5}
        result = req._prepare_kwargs(kwargs)
        assert result is kwargs


class TestParse:
    def _make_request(self):
        req = RequestBase()
        req.client = MagicMock()
        return req

    def test_parses_valid_json_with_result(self):
        req = self._make_request()
        data = {'result': {'someKey': 'value'}, 'invocationInfo': None}
        json_bytes = json.dumps(data).encode('UTF-8')
        response = req._parse(json_bytes)
        assert response is not None
        result = response.get_result()
        # _parse does no normalization; keys are raw from API
        assert result['someKey'] == 'value'

    def test_wraps_result_when_missing(self):
        req = self._make_request()
        data = {'someKey': 'value'}
        json_bytes = json.dumps(data).encode('UTF-8')
        response = req._parse(json_bytes)
        assert response is not None

    def test_no_normalization_in_parse(self):
        req = self._make_request()
        data = {'result': {'camelCase': 1, 'nested-key': {'innerKey': 2}}}
        json_bytes = json.dumps(data).encode('UTF-8')
        response = req._parse(json_bytes)
        result = response.get_result()
        # _parse passes raw keys through — normalization happens lazily in cleanup_data
        assert 'camelCase' in result
        assert 'nested-key' in result
        assert 'innerKey' in result['nested-key']

    def test_invalid_utf8_raises(self):
        req = self._make_request()
        with pytest.raises(YandexMusicError):
            req._parse(b'\xff\xfe')

    def test_invalid_json_raises(self):
        req = self._make_request()
        with pytest.raises(YandexMusicError, match='Invalid server response'):
            req._parse(b'not json')

    def test_preserves_error_fields(self):
        req = self._make_request()
        data = {'error': 'something_wrong', 'errorDescription': 'details'}
        json_bytes = json.dumps(data).encode('UTF-8')
        response = req._parse(json_bytes)
        assert response is not None


class TestHandleErrorResponse:
    def _make_request(self):
        req = RequestBase()
        req.client = MagicMock()
        return req

    def _make_error_body(self, error='test_error', description='test_desc'):
        return json.dumps(
            {
                'error': error,
                'error_description': description,
            }
        ).encode('UTF-8')

    @pytest.mark.parametrize('status_code', [401, 403])
    def test_unauthorized(self, status_code):
        req = self._make_request()
        with pytest.raises(UnauthorizedError):
            req._handle_error_response(status_code, self._make_error_body())

    def test_bad_request(self):
        req = self._make_request()
        with pytest.raises(BadRequestError):
            req._handle_error_response(400, self._make_error_body())

    def test_not_found(self):
        req = self._make_request()
        with pytest.raises(NotFoundError):
            req._handle_error_response(404, self._make_error_body())

    @pytest.mark.parametrize('status_code', [409, 413])
    def test_network_error_codes(self, status_code):
        req = self._make_request()
        with pytest.raises(NetworkError):
            req._handle_error_response(status_code, self._make_error_body())

    def test_bad_gateway(self):
        req = self._make_request()
        with pytest.raises(NetworkError, match='Bad Gateway'):
            req._handle_error_response(502, self._make_error_body())

    def test_unknown_status_code(self):
        req = self._make_request()
        with pytest.raises(NetworkError):
            req._handle_error_response(500, self._make_error_body())

    def test_unparseable_body(self):
        req = self._make_request()
        with pytest.raises(UnauthorizedError):
            req._handle_error_response(401, b'not json')
