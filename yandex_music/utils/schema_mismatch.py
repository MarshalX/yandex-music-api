"""Расхождения моделей с API."""

import dataclasses
import logging
import re
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Dict, FrozenSet, Iterable, List, Mapping, Optional, Set, Tuple
from urllib.parse import urlencode, urlsplit

from yandex_music.exceptions import SchemaMismatchError
from yandex_music.utils.normalize import _normalize_key

if TYPE_CHECKING:
    from yandex_music.base import ClientType, JSONType

logger = logging.getLogger(__name__)

ISSUES_URL = 'https://github.com/MarshalX/yandex-music-api/issues/new'
ISSUE_TEMPLATE = 'schema-mismatch.yml'

_current_endpoint: ContextVar[Optional[str]] = ContextVar('yandex_music_current_endpoint', default=None)
_reported: Set[Tuple[type, FrozenSet[str], FrozenSet[str]]] = set()

_ID_SEGMENT = re.compile(r'^[\d:_-]*\d[\d:_-]*$|^[0-9a-fA-F-]{16,}$')

_SHAPE_MAX_DEPTH = 3
_SHAPE_MAX_LENGTH = 500
_SCALAR_NAMES: Dict[type, str] = {type(None): 'null', bool: 'bool', int: 'int', float: 'float', str: 'str'}


@dataclass(frozen=True)
class SchemaMismatch:
    """Расхождение модели библиотеки с ответом API.

    Attributes:
        model (:obj:`type`): Класс модели.
        missing_fields (:obj:`frozenset` из :obj:`str`): Обязательные поля, которые не пришли от API или равны null.
        unknown_fields (:obj:`frozenset` из :obj:`str`): Поля от API, которых нет в модели.
        endpoint (:obj:`str`, optional): Метод и путь последнего запроса без параметров и идентификаторов.
        version (:obj:`str`): Версия библиотеки.
        unknown_field_shapes (:obj:`Mapping` из :obj:`str` в :obj:`str`): Структура значений неизвестных полей.
    """

    model: type
    missing_fields: FrozenSet[str] = field(default_factory=frozenset)
    unknown_fields: FrozenSet[str] = field(default_factory=frozenset)
    endpoint: Optional[str] = None
    version: str = ''
    unknown_field_shapes: Mapping[str, str] = field(default_factory=dict, hash=False)

    @property
    def model_name(self) -> str:
        """:obj:`str`: Полное имя класса модели."""
        return f'{self.model.__module__}.{self.model.__name__}'

    def describe(self) -> str:
        """Текстовое описание расхождения.

        Returns:
            :obj:`str`: Описание без пользовательских данных.
        """
        lines = [f'Type: {self.model_name}']
        if len(self.missing_fields) > 0:
            lines.append(f'Missing required fields: {", ".join(sorted(self.missing_fields))}')
        if len(self.unknown_fields) > 0:
            lines.append(f'Unknown fields: {", ".join(sorted(self.unknown_fields))}')
        if len(self.unknown_field_shapes) > 0:
            lines.append('Unknown field shapes:')
            lines.extend(f'  {name}: {self.unknown_field_shapes[name]}' for name in sorted(self.unknown_field_shapes))
        lines.append(f'Endpoint: {self.endpoint if self.endpoint is not None else "unknown"}')
        lines.append(f'Version: {self.version}')
        return '\n'.join(lines)

    def issue_url(self) -> str:
        """Ссылка на создание заполненного GitHub issue.

        Returns:
            :obj:`str`: Ссылка.
        """
        kind = 'Отсутствует обязательное поле' if len(self.missing_fields) > 0 else 'Новое неизвестное поле'
        query = urlencode(
            {
                'template': ISSUE_TEMPLATE,
                'title': f'{kind} от API: {self.model.__name__}',
                'report': self.describe(),
            }
        )
        return f'{ISSUES_URL}?{query}'


SchemaMismatchHandler = Callable[[SchemaMismatch], None]


def describe_shape(value: 'JSONType') -> str:
    """Структура значения из ответа API без самих значений.

    Note:
        Вместо значений выводятся типы, ключи-идентификаторы заменяются на ``{id}``, структуры элементов списка
        объединяются. Например: ``list[{id: int, title: null | str}]``.

    Args:
        value (:obj:`JSONType`): Значение поля из ответа API.

    Returns:
        :obj:`str`: Описание структуры.
    """
    shape = _describe_value(value, 0)
    return shape if len(shape) <= _SHAPE_MAX_LENGTH else f'{shape[: _SHAPE_MAX_LENGTH - 1]}…'


def _describe_value(value: 'JSONType', depth: int) -> str:
    if isinstance(value, dict):
        return _describe_dicts([value], depth)
    if isinstance(value, list):
        if len(value) == 0:
            return 'list[]'
        if depth >= _SHAPE_MAX_DEPTH:
            return 'list[...]'
        dicts = [item for item in value if isinstance(item, dict)]
        variants = {_describe_value(item, depth + 1) for item in value if not isinstance(item, dict)}
        if len(dicts) > 0:
            variants.add(_describe_dicts(dicts, depth + 1))
        return f'list[{" | ".join(sorted(variants))}]'
    return _SCALAR_NAMES.get(type(value), type(value).__name__)


def _describe_dicts(dicts: List[Dict[str, 'JSONType']], depth: int) -> str:
    if depth >= _SHAPE_MAX_DEPTH:
        return '{...}'

    keys: Dict[str, Set[str]] = {}
    for item in dicts:
        for key, value in item.items():
            name = '{id}' if _ID_SEGMENT.match(key) is not None else _normalize_key(key)
            keys.setdefault(name, set()).add(_describe_value(value, depth + 1))
    return '{' + ', '.join(f'{name}: {" | ".join(sorted(types))}' for name, types in keys.items()) + '}'


def sanitize_endpoint(method: str, url: str) -> str:
    """Удаление параметров и идентификаторов из адреса запроса.

    Args:
        method (:obj:`str`): HTTP метод.
        url (:obj:`str`): Адрес запроса.

    Returns:
        :obj:`str`: Метод и путь, где идентификаторы и логины заменены на ``{id}``.
    """
    segments = urlsplit(url).path.split('/')
    for i, segment in enumerate(segments):
        if _ID_SEGMENT.match(segment) is not None or (i > 0 and segments[i - 1] == 'users'):
            segments[i] = '{id}'
    return f'{method.upper()} {"/".join(segments)}'


def set_current_endpoint(method: str, url: str) -> None:
    """Запоминание последнего запроса в текущем контексте.

    Args:
        method (:obj:`str`): HTTP метод.
        url (:obj:`str`): Адрес запроса.
    """
    _ = _current_endpoint.set(sanitize_endpoint(method, url))


def get_current_endpoint() -> Optional[str]:
    """Последний запрос в текущем контексте.

    Returns:
        :obj:`str`, optional: Метод и путь запроса.
    """
    return _current_endpoint.get()


def default_handler(mismatch: SchemaMismatch) -> None:
    """Обработчик по умолчанию: предупреждение в лог со ссылкой на заполненный issue.

    Args:
        mismatch (:obj:`yandex_music.utils.schema_mismatch.SchemaMismatch`): Расхождение.
    """
    logger.warning(
        'API response does not match the library model. Please report it, thank you!\n%s\nReport: %s',
        mismatch.describe(),
        mismatch.issue_url(),
    )


def report_schema_mismatch(
    model: type,
    client: Optional['ClientType'],
    missing_fields: Iterable[str] = (),
    unknown_fields: Iterable[str] = (),
    unknown_values: Optional[Mapping[str, 'JSONType']] = None,
) -> None:
    """Отправка отчёта о расхождении.

    Note:
        Отчёт по одной и той же модели и набору полей отправляется один раз за процесс.

        В строгом режиме клиента (``client.strict``) отсутствие обязательных полей вызывает исключение.

    Args:
        model (:obj:`type`): Класс модели.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        missing_fields (:obj:`Iterable` из :obj:`str`): Отсутствующие обязательные поля.
        unknown_fields (:obj:`Iterable` из :obj:`str`): Неизвестные поля.
        unknown_values (:obj:`Mapping` из :obj:`str` в :obj:`JSONType`, optional): Значения неизвестных полей, в отчёт
            попадает только их структура.

    Raises:
        :class:`yandex_music.exceptions.SchemaMismatchError`: В строгом режиме при отсутствии обязательных полей.
    """
    from yandex_music import __version__

    mismatch = SchemaMismatch(
        model=model,
        missing_fields=frozenset(missing_fields),
        unknown_fields=frozenset(unknown_fields),
        endpoint=get_current_endpoint(),
        version=__version__,
    )

    if len(mismatch.missing_fields) > 0 and client is not None and client.strict is True:
        raise SchemaMismatchError(mismatch.describe())

    key = (model, mismatch.missing_fields, mismatch.unknown_fields)
    if key in _reported:
        return
    _reported.add(key)

    if unknown_values is not None:
        shapes = {name: describe_shape(unknown_values[name]) for name in mismatch.unknown_fields}
        mismatch = dataclasses.replace(mismatch, unknown_field_shapes=shapes)

    handler = client.on_schema_mismatch if client is not None else None
    if handler is not None:
        handler(mismatch)
    else:
        default_handler(mismatch)


def reset_reported() -> None:
    """Сброс списка уже отправленных отчётов."""
    _reported.clear()
