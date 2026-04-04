"""Совместимость JSON библиотек.

Использует orjson (если установлен) как быстрый drop-in replacement для стандартного json.
Приоритет: orjson > json.

Note:
    orjson — опциональная зависимость. Для установки: ``pip install orjson``.
    Поддерживаемая версия: orjson<=3.10.15 (последняя с поддержкой Python 3.8).

"""

from typing import Any, Union

try:
    import orjson

    def loads(data: Union[bytes, str]) -> Any:
        """Десериализация JSON. Принимает bytes напрямую (без decode)."""
        return orjson.loads(data)

    def dumps(obj: Any) -> str:
        """Сериализация в JSON строку (UTF-8, без ensure_ascii)."""
        return orjson.dumps(obj).decode('UTF-8')

    accepts_bytes = True

except ImportError:
    import json

    def loads(data: Union[bytes, str]) -> Any:
        """Десериализация JSON."""
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        return json.loads(data)

    def dumps(obj: Any) -> str:
        """Сериализация в JSON строку (UTF-8, без экранирования не-ASCII символов)."""
        return json.dumps(obj, ensure_ascii=False)

    accepts_bytes = False
