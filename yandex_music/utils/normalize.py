"""Утилиты для нормализации ключей API-ответов."""

import keyword
import re
from functools import lru_cache

_CAMEL_RE1 = re.compile('(.)([A-Z][a-z]+)')
_CAMEL_RE2 = re.compile('([a-z0-9])([A-Z])')

RESERVED_NAMES = frozenset([*keyword.kwlist, 'ClientType'])


@lru_cache(maxsize=2048)
def _convert_camel_to_snake(text: str) -> str:
    """Конвертация CamelCase в SnakeCase.

    Args:
        text (:obj:`str`): Название переменной в CamelCase.

    Returns:
        :obj:`str`: Название переменной в SnakeCase.
    """
    s = _CAMEL_RE1.sub(r'\1_\2', text)
    return _CAMEL_RE2.sub(r'\1_\2', s).lower()


@lru_cache(maxsize=2048)
def _normalize_key(key: str) -> str:
    """Нормализация имени переменной пришедшей с API.

    Note:
        В названии переменной заменяет "-" на "_", конвертирует в SnakeCase, если название является
        зарезервированным словом или "client" - добавляет "_" в конец. Если название переменной начинается с цифры -
        добавляет в начало "_".

    Args:
        key (:obj:`str`): Название переменной.

    Returns:
        :obj:`str`: Нормализованное название переменной.
    """
    key = _convert_camel_to_snake(key.replace('-', '_'))

    if key in RESERVED_NAMES:
        key += '_'

    if key and key[0].isdigit():
        key = '_' + key

    return key
