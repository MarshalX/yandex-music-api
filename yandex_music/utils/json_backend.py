"""Подключаемые JSON библиотеки.

Вся сериализация и десериализация JSON в библиотеке (ответы API, тела запросов, ``to_json`` моделей,
фреймы Ynison) выполняется через объект, реализующий протокол :class:`JsonBackend`.

Из коробки поддерживаются `orjson`, `pydantic-core`, `ujson` и стандартный :mod:`json`. Если бэкенд
не указан явно, используется самый быстрый из установленных в порядке приоритета:
orjson, pydantic-core, ujson, json.

Бэкенд можно указать для конкретного клиента или глобально::

    from yandex_music import Client
    from yandex_music.utils.json_backend import OrjsonBackend, set_default_json_backend

    client = Client(token, json_backend=OrjsonBackend())

    set_default_json_backend(OrjsonBackend())

Для подключения своей библиотеки достаточно объекта с методами ``loads`` и ``dumps``::

    import msgspec

    class MsgspecBackend:
        def loads(self, data):
            return msgspec.json.decode(data)

        def dumps(self, obj):
            return msgspec.json.encode(obj).decode('UTF-8')

Note:
    Сторонние библиотеки опциональны. Для установки: ``pip install yandex-music[orjson]``,
    ``pip install yandex-music[pydantic-core]`` или ``pip install yandex-music[ujson]``.

"""

from typing import Any, Callable, List, Optional, Protocol, Union


class JsonBackend(Protocol):
    """Протокол JSON библиотеки.

    Note:
        ``loads`` при некорректных данных должен выбрасывать :class:`ValueError` или его наследника.
        ``dumps`` должен возвращать строку без экранирования не-ASCII символов.
    """

    def loads(self, data: Union[bytes, str]) -> Any:
        """Десериализация JSON.

        Args:
            data (:obj:`bytes` | :obj:`str`): JSON документ. Байты в кодировке UTF-8.

        Returns:
            Десериализованный объект.
        """
        ...

    def dumps(self, obj: Any) -> str:
        """Сериализация в JSON строку.

        Args:
            obj: Объект для сериализации.

        Returns:
            :obj:`str`: JSON строка.
        """
        ...


class StdlibBackend:
    """Стандартная библиотека :mod:`json`."""

    def __init__(self) -> None:
        import json

        self._json = json

    def loads(self, data: Union[bytes, str]) -> Any:
        """Десериализация JSON."""
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        return self._json.loads(data)

    def dumps(self, obj: Any) -> str:
        """Сериализация в JSON строку."""
        return self._json.dumps(obj, ensure_ascii=False)


class OrjsonBackend:
    """Библиотека `orjson <https://github.com/ijl/orjson>`_.

    Note:
        Поддерживаемая версия: orjson<=3.10.15 (последняя с поддержкой Python 3.8).

        В отличие от остальных бэкендов не сериализует ключи словарей, отличные от строк,
        и целые числа больше 64 бит.

    Raises:
        :class:`ImportError`: Если orjson не установлен.
    """

    def __init__(self) -> None:
        import orjson

        self._orjson = orjson

    def loads(self, data: Union[bytes, str]) -> Any:
        """Десериализация JSON."""
        return self._orjson.loads(data)

    def dumps(self, obj: Any) -> str:
        """Сериализация в JSON строку."""
        return self._orjson.dumps(obj).decode('UTF-8')


class PydanticCoreBackend:
    """Библиотека `pydantic-core <https://github.com/pydantic/pydantic-core>`_.

    Raises:
        :class:`ImportError`: Если pydantic-core не установлен.
    """

    def __init__(self) -> None:
        import pydantic_core

        self._pydantic_core = pydantic_core

    def loads(self, data: Union[bytes, str]) -> Any:
        """Десериализация JSON."""
        return self._pydantic_core.from_json(data)

    def dumps(self, obj: Any) -> str:
        """Сериализация в JSON строку."""
        return self._pydantic_core.to_json(obj).decode('UTF-8')


class UjsonBackend:
    """Библиотека `ujson <https://github.com/ultrajson/ultrajson>`_.

    Raises:
        :class:`ImportError`: Если ujson не установлен.
    """

    def __init__(self) -> None:
        import ujson

        self._ujson = ujson

    def loads(self, data: Union[bytes, str]) -> Any:
        """Десериализация JSON."""
        return self._ujson.loads(data)

    def dumps(self, obj: Any) -> str:
        """Сериализация в JSON строку."""
        return self._ujson.dumps(obj, ensure_ascii=False)


_PRIORITY: List[Callable[[], JsonBackend]] = [OrjsonBackend, PydanticCoreBackend, UjsonBackend]

_detected_backend: Optional[JsonBackend] = None
_default_backend: Optional[JsonBackend] = None


def detect_json_backend() -> JsonBackend:
    """Выбор самой быстрой из установленных JSON библиотек.

    Note:
        Порядок приоритета: orjson, pydantic-core, ujson, json. Результат кэшируется.

    Returns:
        :obj:`JsonBackend`: Бэкенд.
    """
    global _detected_backend  # noqa: PLW0603

    if _detected_backend is None:
        for factory in _PRIORITY:
            try:
                _detected_backend = factory()
                break
            except ImportError:
                continue
        else:
            _detected_backend = StdlibBackend()

    return _detected_backend


def get_default_json_backend() -> JsonBackend:
    """Получение глобального бэкенда.

    Returns:
        :obj:`JsonBackend`: Бэкенд, установленный через :func:`set_default_json_backend`,
            или автоматически выбранный через :func:`detect_json_backend`.
    """
    if _default_backend is not None:
        return _default_backend
    return detect_json_backend()


def set_default_json_backend(backend: Optional[JsonBackend]) -> None:
    """Установка глобального бэкенда.

    Note:
        Используется везде, где бэкенд не указан явно: клиентами, моделями без клиента, Ynison.

    Args:
        backend (:obj:`JsonBackend`, optional): Бэкенд. :obj:`None` возвращает автоматический выбор.
    """
    global _default_backend  # noqa: PLW0603

    _default_backend = backend
