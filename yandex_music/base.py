"""Базовые классы."""

import logging
import sys
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
    get_type_hints,
)

from typing_extensions import Self, TypeGuard, get_args, get_origin

from yandex_music.utils import model
from yandex_music.utils.normalize import RESERVED_NAMES, _normalize_key

if TYPE_CHECKING:
    from yandex_music import Client, ClientAsync
    from yandex_music._client_base import ClientBase

from yandex_music.utils.json_backend import get_default_json_backend

logger = logging.getLogger(__name__)
new_issue_by_template_url = 'https://bit.ly/3dsFxyH'


JSONType = Union[Dict[str, 'JSONType'], Sequence['JSONType'], str, int, float, bool, None]
ClientType = Union['Client', 'ClientAsync', 'ClientBase']
ModelFieldType = Union[
    Dict[str, 'ModelFieldType'], Sequence['ModelFieldType'], 'YandexMusicModel', str, int, float, bool, None
]
ModelFieldMap = Dict[str, 'ModelFieldType']
MapTypeToDeJson = Dict[str, Callable[['JSONType', 'ClientType'], Optional['YandexMusicModel']]]
NestedConverter = Callable[[Any, 'ClientType'], Any]

_nested_plans: Dict[type, List[Tuple[str, NestedConverter]]] = {}
_annotations_namespace: Dict[str, Any] = {}


def _get_annotations_namespace() -> Dict[str, Any]:
    if len(_annotations_namespace) == 0:
        import yandex_music
        from yandex_music._client_base import ClientBase

        _annotations_namespace.update(vars(yandex_music))
        _annotations_namespace['ClientBase'] = ClientBase

    return _annotations_namespace


def _unwrap_optional(type_: Any) -> Any:
    if get_origin(type_) is Union:
        args = [arg for arg in get_args(type_) if arg is not type(None)]
        return args[0] if len(args) == 1 else None

    return type_


def _de_nested_list(converter: NestedConverter) -> NestedConverter:
    def convert(value: Any, client: 'ClientType') -> List[Any]:
        if not isinstance(value, list):
            return []
        return [converter(item, client) for item in cast('List[Any]', value)]

    return convert


def _de_nested_dict(converter: NestedConverter) -> NestedConverter:
    def convert(value: Any, client: 'ClientType') -> Dict[str, Any]:
        if not isinstance(value, dict):
            return {}
        result: Dict[str, Any] = {}
        for key, item in cast('Dict[str, Any]', value).items():
            converted = converter(item, client)
            if converted is not None:
                result[key] = converted
        return result

    return convert


def _build_nested_converter(type_: Any) -> Optional[NestedConverter]:
    type_ = _unwrap_optional(type_)
    if isinstance(type_, type) and issubclass(type_, YandexMusicModel):
        return type_.de_json

    origin = get_origin(type_)
    if origin is list:
        (item_type,) = get_args(type_)
        item_type = _unwrap_optional(item_type)
        if isinstance(item_type, type) and issubclass(item_type, YandexMusicModel):
            return item_type.de_list
        item_converter = _build_nested_converter(item_type)
        return _de_nested_list(item_converter) if item_converter is not None else None

    if origin is dict:
        _, value_type = get_args(type_)
        value_converter = _build_nested_converter(value_type)
        return _de_nested_dict(value_converter) if value_converter is not None else None

    return None


class YandexMusicObject:
    """Базовый класс для всех классов библиотеки."""


@model
class YandexMusicModel(YandexMusicObject):
    """Базовый класс для всех моделей библиотеки."""

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item: Any) -> Any:
        return self.__dict__[item]

    @staticmethod
    def report_unknown_fields_callback(klass: type, unknown_fields: 'set[str]') -> None:
        """Обратный вызов для обработки неизвестных полей."""
        logger.warning(
            'Found unknown fields received from API! Please copy warn message '
            'and send to %s (GitHub issue), thank you!',
            new_issue_by_template_url,
        )
        logger.warning('Type: %s.%s; fields: %s', klass.__module__, klass.__name__, unknown_fields)

    @staticmethod
    def is_dict_model_data(data: JSONType) -> TypeGuard[Dict[str, JSONType]]:
        """Проверка на соответствие данных словарю.

        Args:
            data (:obj:`JSONType`): Данные для проверки.

        Returns:
            :obj:`bool`: Валидны ли данные.
        """
        return bool(data) and isinstance(data, dict)

    @staticmethod
    def valid_client(client: Optional['ClientType']) -> TypeGuard['Client']:
        """Проверка что клиент передан и является синхронным.

        Args:
            client (:obj:`Optional['ClientType']`): Клиент для проверки.

        Returns:
            :obj:`bool`: Синхронный ли клиент.
        """
        from yandex_music import Client

        return isinstance(client, Client)

    @staticmethod
    def valid_async_client(client: Optional['ClientType']) -> TypeGuard['ClientAsync']:
        """Проверка что клиент передан и является асинхронным.

        Args:
            client (:obj:`Optional['ClientType']`): Клиент для проверки.

        Returns:
            :obj:`bool`: Асинхронный ли клиент.
        """
        from yandex_music import ClientAsync

        return isinstance(client, ClientAsync)

    @staticmethod
    def is_array_model_data(data: JSONType) -> TypeGuard[List[Dict[str, JSONType]]]:
        """Проверка на соответствие данных массиву словарей.

        Args:
            data (:obj:`JSONType`): Данные для проверки.

        Returns:
            :obj:`bool`: Валидны ли данные.
        """
        return bool(data) and isinstance(data, list) and all(isinstance(item, dict) for item in data)

    @classmethod
    def cleanup_data(cls, data: JSONType, client: Optional['ClientType']) -> Dict[str, Any]:
        """Нормализует ключи и удаляет незадекларированные поля для текущей модели из сырых данных.

        Note:
            Нормализация ключей (camelCase → snake_case) выполняется лениво на текущем уровне,
            без рекурсивного обхода вложенных структур. Фильтрует только словарь поле:значение.
            Иначе вернёт пустой :obj:`dict`.

        Args:
            data (:obj:`JSONType`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`dict`: Отфильтрованные данные с нормализованными ключами.
        """
        if not YandexMusicModel.is_dict_model_data(data):
            return {}

        known = cls.__dataclass_fields__
        result: Dict[str, Any] = {}
        report = client is not None and client.report_unknown_fields
        unknown_keys: Optional[Set[str]] = set() if report else None

        for k, v in data.items():
            nk = _normalize_key(k)
            if nk in known:
                result[nk] = v
            elif unknown_keys is not None:
                unknown_keys.add(nk)

        if unknown_keys is not None and len(unknown_keys) > 0:
            cls.report_unknown_fields_callback(cls, unknown_keys)

        return result

    @classmethod
    def nested_plan(cls) -> List[Tuple[str, NestedConverter]]:
        """Построение плана десериализации вложенных объектов по аннотациям полей.

        Note:
            Учитываются поля вида ``Model``, ``List[Model]``, ``Dict[str, Model]`` и их вложенные
            комбинации, обёрнутые в ``Optional``. Остальные поля (примитивы, ``Union`` нескольких
            типов, ``Any``) остаются без изменений. План строится один раз на класс и кешируется.

        Returns:
            :obj:`list` из :obj:`tuple`: Пары из имени поля и функции его десериализации.
        """
        cached = _nested_plans.get(cls)
        if cached is not None:
            return cached

        hints = get_type_hints(cls, vars(sys.modules[cls.__module__]), _get_annotations_namespace())
        plan: List[Tuple[str, NestedConverter]] = []
        for name in cls.__dataclass_fields__:
            if name == 'client':
                continue
            converter = _build_nested_converter(hints.get(name))
            if converter is not None:
                plan.append((name, converter))

        _nested_plans[cls] = plan
        return plan

    @classmethod
    def de_nested(cls, cls_data: Dict[str, Any], client: 'ClientType', exclude: Collection[str] = ()) -> Dict[str, Any]:
        """Десериализация вложенных объектов в очищенных данных.

        Note:
            Используется в переопределённом :meth:`de_json`, когда часть полей требует особой обработки.
            Такие поля передаются в ``exclude`` и обрабатываются вручную.

        Args:
            cls_data (:obj:`dict`): Данные после :meth:`cleanup_data`.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
            exclude (:obj:`Collection` из :obj:`str`, optional): Поля, которые не нужно обрабатывать.

        Returns:
            :obj:`dict`: Те же данные с десериализованными вложенными объектами.
        """
        for name, converter in cls.nested_plan():
            if name not in exclude:
                cls_data[name] = converter(cls_data.get(name), client)

        return cls_data

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional[Self]:
        """Десериализация объекта.

        Note:
            Вложенные объекты десериализуются автоматически по аннотациям полей (см. :meth:`nested_plan`).
            Переопределяется в дочерних классах только для полей с особой логикой.

        Args:
            data (:obj:`JSONType`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.YandexMusicModel`: Десериализованный объект.
        """
        if not cls.is_dict_model_data(data):
            return None

        kwargs = cls.de_nested(cls.cleanup_data(data, client), client)
        kwargs['client'] = client
        return cls(**kwargs)

    @classmethod
    def de_list(cls, data: JSONType, client: 'ClientType') -> Sequence[Self]:
        """Десериализация списка объектов.

        Note:
            Переопределяется в дочерних классах, если необходимо.

            Например, в сложных объектах где есть вариации подтипов.

        Args:
            data (:obj:`JSONType`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.YandexMusicModel`: Список десериализованных объектов.
        """
        if not isinstance(data, list) or len(data) == 0:
            return []

        result: List[Self] = []
        for item in data:
            if isinstance(item, dict):
                obj = cls.de_json(item, client)
                if obj is not None:
                    result.append(obj)
        return result

    def to_json(self, for_request: bool = False) -> str:
        """Сериализация объекта.

        Args:
            for_request (:obj:`bool`): Подготовить ли объект для отправки в теле запроса.

        Note:
            Используется JSON библиотека клиента объекта, а при его отсутствии глобальная.

        Returns:
            :obj:`str`: Сериализованный в JSON объект.
        """
        client = getattr(self, 'client', None)
        if self.valid_client(client) or self.valid_async_client(client):
            return client.request.json_backend.dumps(self.to_dict(for_request))
        return get_default_json_backend().dumps(self.to_dict(for_request))

    def to_dict(self, for_request: bool = False) -> JSONType:
        """Рекурсивная сериализация объекта.

        Args:
            for_request (:obj:`bool`): Перевести ли обратно все поля в camelCase и игнорировать зарезервированные слова.

        Note:
            Исключает из сериализации `client` и `_id_attrs` необходимые в `__eq__`.

            К зарезервированным словам добавляет "_" в конец.

        Returns:
            :obj:`dict`: Сериализованный в dict объект.
        """

        def parse(val: Union['YandexMusicModel', JSONType]) -> JSONType:
            if isinstance(val, YandexMusicModel):
                return val.to_dict(for_request)
            if isinstance(val, list):
                return [parse(it) for it in val]
            if isinstance(val, dict):
                return {key: parse(value) for key, value in val.items()}
            return val

        data = self.__dict__.copy()
        data.pop('client', None)
        data.pop('_id_attrs', None)

        if for_request:
            new_data: Dict[str, Any] = {}
            for k, v in data.items():
                camel_case = ''.join(word.title() for word in k.split('_'))
                camel_case = camel_case[0].lower() + camel_case[1:]
                new_data[camel_case] = v
            data = new_data
        else:
            for k in list(data):
                if k in RESERVED_NAMES:
                    data[f'{k}_'] = data.pop(k)

        return parse(data)

    def _get_id_attrs(self) -> Tuple[object, ...]:
        """Получение ключевых атрибутов объекта.

        Returns:
            :obj:`tuple`: Ключевые атрибуты объекта для сравнения.
        """
        return cast('Tuple[object, ...]', getattr(self, '_id_attrs', ()))

    def __eq__(self, other: object) -> bool:
        """Проверка на равенство двух объектов.

        Note:
            Проверка осуществляется по определённым атрибутам классов, перечисленных в множестве `_id_attrs`.

        Returns:
            :obj:`bool`: Одинаковые ли объекты (по содержимому).
        """
        if isinstance(other, self.__class__):
            return self._get_id_attrs() == other._get_id_attrs()
        return super().__eq__(other)

    def __hash__(self) -> int:
        """Реализация хеш-функции на основе ключевых атрибутов.

        Note:
            Так как перечень ключевых атрибутов хранится в виде множества, для вычисления хеша он замораживается.

        Returns:
            :obj:`int`: Хеш объекта.
        """
        id_attrs = self._get_id_attrs()
        if len(id_attrs) == 0:
            return super().__hash__()

        frozen_attrs = tuple(frozenset(attr) if isinstance(attr, list) else attr for attr in id_attrs)
        return hash((self.__class__, frozen_attrs))
