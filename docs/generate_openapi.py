"""Генерация OpenAPI-спецификации Yandex Music API на основе библиотеки.

Каждый публичный метод ClientAsync вызывается с аргументами-заглушками, а первый
HTTP-запрос перехватывается подменённым Request. Путь, параметры и тело запроса
берутся из перехваченного запроса, схема ответа из аннотации возвращаемого типа
и аннотаций полей моделей. Описания берутся из docstring.

Результат записывается в source/_extra/api/openapi.json и публикуется по адресу /api/.
"""

import asyncio
import collections.abc
import contextlib
import dataclasses
import inspect
import json
import re
import sys
import typing
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from typing_extensions import override

sys.path.insert(0, str(Path(__file__).parent.parent))

import yandex_music
from yandex_music import ClientAsync, YandexMusicModel
from yandex_music._client_base import ClientBase
from yandex_music.utils.request_async import Request

OUTPUT = Path(__file__).parent / 'source' / '_extra' / 'api' / 'openapi.json'
BASE_URL = 'https://api.music.yandex.net'
DOCS_URL = 'https://ym.marshal.dev'
GITHUB_URL = 'https://github.com/MarshalX/yandex-music-api'
AUTHOR_URL = 'https://github.com/MarshalX'
SKIPPED_METHODS = {'init', 'request', 'device_auth'}
NUMERIC_TOKEN_BASE = 900000

JSONSchema = Dict[str, Any]
NAMESPACE: Dict[str, Any] = {**vars(yandex_music), 'ClientBase': ClientBase}
PRIMITIVES = {str: 'string', bool: 'boolean', int: 'integer', float: 'number'}
ARRAY_ORIGINS = (list, tuple, collections.abc.Sequence)
INSTALL_COMMENT = '# pip install yandex-music\n'
TAG_ICONS = {
    'AccountMixin': '👤',
    'AlbumsMixin': '💿',
    'ArtistsMixin': '🎤',
    'ClipsMixin': '🎬',
    'ConcertsMixin': '🎫',
    'CreditsMixin': '👥',
    'DeviceAuthMixin': '🔑',
    'DisclaimersMixin': '🚫',
    'LabelsMixin': '🏢',
    'LandingMixin': '🏠',
    'LikesMixin': '👍',
    'MetatagsMixin': '🔖',
    'MusicHistoryMixin': '🕘',
    'PinsMixin': '📌',
    'PlaylistsMixin': '🎶',
    'PresavesMixin': '⏳',
    'QueueMixin': '📋',
    'RadioMixin': '📻',
    'RotorSessionsMixin': '📡',
    'SearchMixin': '🔍',
    'TracksMixin': '🎵',
    'WaveMixin': '🌊',
}

DESCRIPTION = f"""\
Неофициальное описание API Яндекс Музыки, сгенерированное автоматически из Python-библиотеки
**[yandex-music]({GITHUB_URL})**. Все методы ниже уже реализованы в библиотеке: синхронный
и асинхронный клиенты, типизированные модели ответов, [Ynison]({DOCS_URL}/ynison) и [сессии радио]({DOCS_URL}/radio).

```bash
pip install yandex-music
```

```python
from yandex_music import Client

client = Client('TOKEN').init()
client.users_likes_tracks()[0].fetch_track().download('example.mp3')
```

- 📖 [Документация библиотеки]({DOCS_URL})
- ⭐ [Исходный код на GitHub]({GITHUB_URL})
- 📦 [Пакет на PyPI](https://pypi.org/project/yandex-music)
- 💬 [Telegram-чат сообщества](https://t.me/yandex_music_api)

## Ограничения

Описание построено автоматически по коду библиотеки, поэтому возможны неточности:

- Имена полей ответов приведены к camelCase. Часть ключей API на самом деле в kebab-case, например `bar-below`.
- Поля тела запроса описаны как строки, без точных типов.
- В примерах кода вместо значений аргументов указано `...`.
- Если один эндпоинт используют несколько методов библиотеки, он описан один раз,
  а остальные методы перечислены в поле `x-library-methods`.
- Отправка запросов прямо со страницы отключена, для вызовов используйте библиотеку.

Нашли ошибку? Создайте [issue на GitHub]({GITHUB_URL}/issues).

Автор: [Ilya (Marshal)]({AUTHOR_URL}) 🦁

Если библиотека или это описание пригодились, поставьте ⭐ [репозиторию на GitHub]({GITHUB_URL}).
"""


class CapturedError(Exception):
    """Прерывает метод клиента после перехвата первого запроса."""


@dataclasses.dataclass
class Call:
    """Перехваченный HTTP-запрос."""

    method: str
    url: str
    params: Dict[str, Any]
    body: Dict[str, Any]


@dataclasses.dataclass
class Method:
    """Метод клиента и сведения о нём из сигнатуры и docstring."""

    name: str
    func: Callable[..., Any]
    hints: Dict[str, Any]
    signature: inspect.Signature
    arg_docs: Dict[str, str]

    def python_name(self, key: str) -> str:
        """Имя аргумента метода, соответствующее ключу запроса."""
        return next((name for name in self.signature.parameters if key in (name, camel_case(name))), key)


class RecordingRequest(Request):
    """Request, который записывает запрос вместо его отправки."""

    def __init__(self) -> None:
        """Создаёт Request с пустым списком запросов."""
        super().__init__()
        self.calls: List[Call] = []

    @override
    async def _request_wrapper(self, *args: Any, **kwargs: Any) -> bytes:
        params = kwargs.get('params')
        body = kwargs.get('data', kwargs.get('json'))
        self.calls.append(
            Call(
                method=str(args[0]).lower(),
                url=str(args[1]),
                params=params if isinstance(params, dict) else {},
                body=body if isinstance(body, dict) else {},
            )
        )
        raise CapturedError


class Placeholder(str):
    """Заглушка аргумента, которая попадает в URL как `{name}`."""

    __slots__ = ()

    def to_dict(self, **_options: Any) -> Dict[str, Any]:
        """Заглушка для аргументов-моделей, которые сериализуются в теле запроса."""
        return {}


def camel_case(name: str) -> str:
    """Перевод имени из snake_case в camelCase."""
    first, *rest = name.rstrip('_').split('_')
    return first + ''.join(part.title() for part in rest)


def is_sequence(type_: Any) -> bool:
    """Является ли аннотация списком или кортежем."""
    origin: object = typing.get_origin(type_)
    return origin in (list, tuple)


def placeholder_for(token: str, type_: Any) -> Any:
    """Значение-заглушка, повторяющее форму аннотации аргумента."""
    origin: object = typing.get_origin(type_)
    args = typing.get_args(type_)
    if origin is typing.Union:
        options = [arg for arg in args if arg is not type(None)]
        option = next((arg for arg in options if is_sequence(arg)), options[0])
        return placeholder_for(token, option)
    if origin is list:
        return [placeholder_for(token, args[0] if len(args) > 0 else str)]
    if origin is tuple:
        return tuple(placeholder_for(token, arg) for arg in args)
    if type_ is bool:
        return True
    return Placeholder(token)


def strip_roles(text: str) -> str:
    """Замена ролей Sphinx вида :obj:`False` на Markdown-код."""
    return re.sub(r':\w+:`~?([^`]+)`', r'`\1`', text)


def split_docstring(doc: Optional[str]) -> Tuple[str, str]:
    """Краткое и подробное описание из docstring без секций Args/Returns/..."""
    text = strip_roles(inspect.cleandoc(doc if doc is not None else ''))
    head = re.split(r'\n\s*(?:Args|Returns|Raises|Attributes|Note|Notes|Warning|Example|Examples):', text)[0]
    summary, _, description = head.strip().partition('\n\n')
    return ' '.join(summary.split()), description.strip()


def parse_docstring_section(doc: Optional[str], section: str) -> Dict[str, str]:
    """Описания элементов секции Google-style docstring, например `Args` или `Attributes`."""
    text = strip_roles(inspect.cleandoc(doc if doc is not None else ''))
    match = re.search(rf'^{section}:\n((?:[ ]{{4}}.*\n?|\n)*)', text, re.MULTILINE)
    if match is None:
        return {}

    result: Dict[str, str] = {}
    current = None
    for line in match.group(1).splitlines():
        item = re.match(r'^[ ]{4}(\w+) \(.*?\)(?:, optional)?:\s*(.*)$', line)
        if item is not None:
            current = item.group(1)
            result[current] = item.group(2)
        elif current is not None and line.startswith(' ' * 8):
            result[current] += ' ' + line.strip()
    return result


def type_hints(obj: Any) -> Dict[str, Any]:
    """Аннотации объекта с разрешёнными строковыми ссылками на модели."""
    module: str = obj.__module__
    return typing.get_type_hints(obj, vars(sys.modules[module]), NAMESPACE)


def split_url(url: str) -> Tuple[str, str]:
    """Разделение URL на сервер и путь без query-параметров."""
    match = re.match(r'(https?://[^/]+)(/[^?]*)?', url)
    if match is None:
        return BASE_URL, url
    path: Optional[str] = match.group(2)
    return match.group(1), path if path is not None else '/'


def code_samples(name: str, required: List[str]) -> List[JSONSchema]:
    """Примеры вызова метода через синхронный и асинхронный клиенты библиотеки."""
    arguments = ', '.join(f'{arg}=...' for arg in required)
    sync = (
        f'{INSTALL_COMMENT}from yandex_music import Client\n\n'
        "client = Client('TOKEN').init()\n"
        f'client.{name}({arguments})'
    )
    async_ = (
        f'{INSTALL_COMMENT}from yandex_music import ClientAsync\n\n'
        "client = await ClientAsync('TOKEN').init()\n"
        f'await client.{name}({arguments})'
    )
    return [
        {'lang': 'python', 'label': 'yandex-music', 'source': sync},
        {'lang': 'python', 'label': 'yandex-music (async)', 'source': async_},
    ]


def method_docs_url(func: Callable[..., Any]) -> str:
    """Ссылка на документацию метода синхронного клиента."""
    module = func.__module__.replace('._client_async.', '._client.')
    return f'{DOCS_URL}/{module}/#{module}.{func.__qualname__}'


class SchemaBuilder:
    """Построение JSON Schema по аннотациям типов и моделям библиотеки."""

    def __init__(self) -> None:
        """Создаёт построитель с пустым набором схем моделей."""
        self.schemas: Dict[str, JSONSchema] = {}

    def build(self, type_: Any) -> JSONSchema:
        """Схема для аннотации типа. Модели добавляются в components и подключаются через $ref."""
        origin: object = typing.get_origin(type_)
        args = typing.get_args(type_)
        if origin is typing.Union:
            return self.build_union(args)
        if origin is not None:
            return self.build_generic(origin, args)
        if type_ in PRIMITIVES:
            return {'type': PRIMITIVES[type_]}
        if inspect.isclass(type_) and issubclass(type_, YandexMusicModel):
            self.add_model(type_)
            return {'$ref': f'#/components/schemas/{type_.__name__}'}
        return {}

    def build_union(self, args: Tuple[Any, ...]) -> JSONSchema:
        """Схема для Union и Optional."""
        schemas = [self.build(arg) for arg in args if arg is not type(None)]
        if len(schemas) == 1:
            return schemas[0]
        if all(list(schema) == ['type'] for schema in schemas):
            return {'type': [schema['type'] for schema in schemas]}
        return {'anyOf': schemas}

    def build_generic(self, origin: object, args: Tuple[Any, ...]) -> JSONSchema:
        """Схема для List, Dict и Literal."""
        if origin in ARRAY_ORIGINS:
            return {'type': 'array', 'items': self.build(args[0]) if len(args) > 0 else {}}
        if origin is dict:
            return {'type': 'object', 'additionalProperties': self.build(args[1]) if len(args) > 1 else {}}
        if origin is typing.Literal:
            return {'enum': list(args)}
        return {}

    def add_model(self, cls: type) -> None:
        """Добавление схемы модели и всех вложенных моделей."""
        name = cls.__name__
        if name in self.schemas:
            return
        self.schemas[name] = {}

        hints = type_hints(cls)
        field_docs = parse_docstring_section(cls.__doc__, 'Attributes')
        properties: Dict[str, JSONSchema] = {}
        required: List[str] = []
        for field in dataclasses.fields(cls):
            if field.name == 'client' or field.name.startswith('_'):
                continue
            key = camel_case(field.name)
            schema = self.build(hints.get(field.name, Any))
            if field.name in field_docs:
                schema = {**schema, 'description': field_docs[field.name]}
            properties[key] = schema
            if field.default is dataclasses.MISSING and field.default_factory is dataclasses.MISSING:
                required.append(key)

        summary, _ = split_docstring(cls.__doc__)
        model: JSONSchema = {'type': 'object', 'description': summary, 'properties': properties}
        if len(required) > 0:
            model['required'] = required
        self.schemas[name] = model


class SpecBuilder:
    """Построение OpenAPI-спецификации по методам ClientAsync."""

    def __init__(self) -> None:
        """Создаёт клиент с перехватывающим Request."""
        self.request = RecordingRequest()
        self.client = ClientAsync(request=self.request)
        self.schemas = SchemaBuilder()
        self.paths: Dict[str, Dict[str, JSONSchema]] = {}
        self.tags: Dict[str, JSONSchema] = {}
        self.skipped: List[str] = []

    async def capture(self, method: Method, numeric: bool) -> Optional[Call]:
        """Вызов метода с заглушками вместо всех аргументов без значения по умолчанию.

        Числовые заглушки нужны методам, которые приводят аргументы к :obj:`int`,
        после перехвата они заменяются в URL на `{name}`.
        """
        arguments = [
            name
            for name, param in method.signature.parameters.items()
            if param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD) and param.default in (param.empty, None)
        ]
        tokens = {name: str(NUMERIC_TOKEN_BASE + i) if numeric else f'{{{name}}}' for i, name in enumerate(arguments)}
        kwargs = {name: placeholder_for(tokens[name], method.hints.get(name, str)) for name in arguments}

        self.request.calls.clear()
        with contextlib.suppress(CapturedError):
            await method.func(**kwargs)
        if len(self.request.calls) == 0:
            return None

        call = self.request.calls[0]
        if numeric:
            for name, token in tokens.items():
                call.url = call.url.replace(token, f'{{{name}}}')
        return call

    def parameter(self, method: Method, key: str, location: str) -> JSONSchema:
        """Описание path- или query-параметра."""
        name = method.python_name(key)
        schema: JSONSchema = {'type': 'string'}
        if name in method.hints:
            built = self.schemas.build(method.hints[name])
            if location == 'path' or set(built) == {'type'}:
                schema = built
        return {
            'name': key,
            'in': location,
            'required': location == 'path',
            'description': method.arg_docs.get(name, ''),
            'schema': schema,
        }

    def request_body(self, method: Method, call: Call) -> JSONSchema:
        """Описание тела запроса по ключам перехваченного тела."""
        properties = {
            key: {'type': 'string', 'description': method.arg_docs.get(method.python_name(key), '')}
            for key in call.body
        }
        media_type = 'application/x-www-form-urlencoded' if call.method == 'post' else 'application/json'
        return {'content': {media_type: {'schema': {'type': 'object', 'properties': properties}}}}

    def response(self, method: Method) -> JSONSchema:
        """Описание успешного ответа с результатом по аннотации возвращаемого типа."""
        result = self.schemas.build(method.hints.get('return', Any))
        envelope = {
            'type': 'object',
            'properties': {
                'invocationInfo': {'$ref': '#/components/schemas/InvocationInfo'},
                'result': result,
            },
        }
        return {'200': {'description': 'Успешный ответ.', 'content': {'application/json': {'schema': envelope}}}}

    def tag_for(self, func: Callable[..., Any]) -> str:
        """Тег операции по docstring миксина, в котором объявлен метод."""
        mixin: type = getattr(sys.modules[func.__module__], func.__qualname__.split('.')[0])
        if mixin.__name__ not in TAG_ICONS:
            raise KeyError(f'Нет иконки для {mixin.__name__}: добавьте её в TAG_ICONS')

        name, description = split_docstring(mixin.__doc__)
        name = name.rstrip('.')
        tag = {'name': name, 'x-displayName': f'{TAG_ICONS[mixin.__name__]} {name}', 'description': description}
        _ = self.tags.setdefault(name, tag)
        return name

    def operation(self, method: Method, call: Call, server: str, path: str) -> JSONSchema:
        """Описание операции OpenAPI."""
        summary, description = split_docstring(method.func.__doc__)
        docs_link = f'Метод библиотеки: [`Client.{method.name}`]({method_docs_url(method.func)})'
        parameters = [self.parameter(method, key, 'path') for key in re.findall(r'{(\w+)}', path)]
        parameters += [self.parameter(method, key, 'query') for key in call.params]
        required = [
            name
            for name, param in method.signature.parameters.items()
            if param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD) and param.default is param.empty
        ]

        operation: JSONSchema = {
            'operationId': method.name,
            'summary': summary,
            'description': f'{description}\n\n{docs_link}'.strip(),
            'tags': [self.tag_for(method.func)],
        }
        if len(parameters) > 0:
            operation['parameters'] = parameters
        if len(call.body) > 0:
            operation['requestBody'] = self.request_body(method, call)
        operation['responses'] = self.response(method)
        operation['x-codeSamples'] = code_samples(method.name, required)
        if server != BASE_URL:
            operation['servers'] = [{'url': server}]
            no_security: List[JSONSchema] = []
            operation['security'] = no_security
        return operation

    async def add_method(self, name: str, func: Callable[..., Any]) -> None:
        """Перехват запроса метода и добавление операции в спецификацию."""
        method = Method(
            name=name,
            func=func,
            hints=type_hints(func),
            signature=inspect.signature(func),
            arg_docs=parse_docstring_section(func.__doc__, 'Args'),
        )
        try:
            call = await self.capture(method, numeric=False)
        except (ValueError, TypeError):
            call = await self.capture(method, numeric=True)
        if call is None:
            self.skipped.append(name)
            return

        server, path = split_url(call.url)
        methods = self.paths.setdefault(path, {})
        if call.method in methods:
            methods[call.method].setdefault('x-library-methods', []).append(name)
        else:
            methods[call.method] = self.operation(method, call, server, path)

    async def build(self) -> JSONSchema:
        """Сборка спецификации по всем публичным методам клиента."""
        seen: List[object] = []
        for name in sorted(dir(ClientAsync)):
            if name.startswith('_') or name in SKIPPED_METHODS or not name.islower():
                continue
            function: object = getattr(ClientAsync, name)
            if not inspect.iscoroutinefunction(function) or function in seen:
                continue
            seen.append(function)
            await self.add_method(name, getattr(self.client, name))

        _ = self.schemas.build(yandex_music.InvocationInfo)

        return {
            'openapi': '3.1.0',
            'info': {
                'title': 'Yandex Music API',
                'version': yandex_music.__version__,
                'description': DESCRIPTION,
                'contact': {'name': 'Ilya (Marshal)', 'url': AUTHOR_URL},
                'license': {'name': 'LGPL-3.0', 'identifier': 'LGPL-3.0-only'},
            },
            'externalDocs': {'description': 'Документация библиотеки', 'url': DOCS_URL},
            'servers': [{'url': BASE_URL}],
            'security': [{'OAuth': []}],
            'tags': sorted(self.tags.values(), key=lambda tag: tag['name']),
            'paths': dict(sorted(self.paths.items())),
            'components': {
                'securitySchemes': {
                    'OAuth': {
                        'type': 'apiKey',
                        'in': 'header',
                        'name': 'Authorization',
                        'description': 'Значение вида `OAuth <token>`.',
                    }
                },
                'schemas': dict(sorted(self.schemas.schemas.items())),
            },
        }


def main() -> None:
    """Генерация и запись спецификации."""
    builder = SpecBuilder()
    spec = asyncio.run(builder.build())

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    _ = OUTPUT.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='UTF-8')

    operations = sum(len(methods) for methods in builder.paths.values())
    print(f'OpenAPI: {len(builder.paths)} путей, {operations} операций, {len(builder.schemas.schemas)} схем')
    for name in builder.skipped:
        print(f'  без запроса: {name}')


if __name__ == '__main__':
    main()
