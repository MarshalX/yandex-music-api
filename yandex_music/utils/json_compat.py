"""Совместимость JSON библиотек.

Note:
    Устарело и будет удалено в следующей мажорной версии. Используйте :mod:`yandex_music.utils.json_backend`.

"""

import warnings
from typing import Any, Union

from yandex_music.utils.json_backend import get_default_json_backend

warnings.warn(
    'yandex_music.utils.json_compat is deprecated, use yandex_music.utils.json_backend instead',
    DeprecationWarning,
    stacklevel=2,
)


def loads(data: Union[bytes, str]) -> Any:
    """Десериализация JSON глобальным бэкендом."""
    return get_default_json_backend().loads(data)


def dumps(obj: Any) -> str:
    """Сериализация в JSON строку глобальным бэкендом."""
    return get_default_json_backend().dumps(obj)
