import dataclasses
import keyword
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Tuple, Union, cast

from typing_extensions import Self, TypeGuard

from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, ClientAsync

ujson: bool = False
try:
    import ujson as json

    ujson = True
except ImportError:
    import json

reserved_names = keyword.kwlist

logger = logging.getLogger(__name__)
new_issue_by_template_url = 'https://bit.ly/3dsFxyH'


JSONType = Union[Dict[str, 'JSONType'], Sequence['JSONType'], str, int, float, bool, None]
ClientType = Union['Client', 'ClientAsync']
ModelFieldType = Union[
    Dict[str, 'ModelFieldType'], Sequence['ModelFieldType'], 'YandexMusicModel', str, int, float, bool, None
]
ModelFieldMap = Dict[str, 'ModelFieldType']
MapTypeToDeJson = Dict[str, Callable[['JSONType', 'ClientType'], Optional['YandexMusicModel']]]


class YandexMusicObject:
    """Базовый класс для всех классов библиотеки."""


@model
class YandexMusicModel(YandexMusicObject):
    """Базовый класс для всех моделей библиотеки."""

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item: str) -> Any:
        return self.__dict__[item]

    @staticmethod
    def report_unknown_fields_callback(klass: type, unknown_fields: JSONType) -> None:
        """Обратный вызов для обработки неизвестных полей."""
        logger.warning(
            f'Found unknown fields received from API! Please copy warn message '
            f'and send to {new_issue_by_template_url} (GitHub issue), thank you!'
        )
        logger.warning(f'Type: {klass.__module__}.{klass.__name__}; fields: {unknown_fields}')

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
    def cleanup_data(cls, data: JSONType, client: Optional['ClientType']) -> ModelFieldMap:
        """Удаляет незадекларированные поля для текущей модели из сырых данных.

        Note:
            Фильтрует только словарь поле:значение. Иначе вернёт пустой :obj:`dict`.

        Args:
            data (:obj:`JSONType`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`ModelFieldMap`: Отфильтрованные данные.
        """
        if not YandexMusicModel.is_dict_model_data(data):
            return {}

        data = data.copy()

        fields = {f.name for f in dataclasses.fields(cls)}

        cleaned_data: Dict[str, JSONType] = {}
        unknown_data: Dict[str, JSONType] = {}

        for k, v in data.items():
            if k in fields:
                cleaned_data[k] = v
            else:
                unknown_data[k] = v

        if client and client.report_unknown_fields and unknown_data:
            cls.report_unknown_fields_callback(cls, unknown_data)

        return cleaned_data

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional[Self]:
        """Десериализация объекта.

        Note:
            Переопределяется в дочерних классах когда есть вложенные объекты.

        Args:
            data (:obj:`JSONType`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.YandexMusicModel`: Десериализованный объект.
        """
        if not cls.is_dict_model_data(data):
            return None

        return cls(client=client, **cls.cleanup_data(data, client))

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
        if not cls.is_array_model_data(data):
            return []

        items = [cls.de_json(item, client) for item in data]
        return [item for item in items if item is not None]

    def to_json(self, for_request: bool = False) -> str:
        """Сериализация объекта.

        Args:
            for_request (:obj:`bool`): Подготовить ли объект для отправки в теле запроса.

        Returns:
            :obj:`str`: Сериализованный в JSON объект.
        """
        return json.dumps(self.to_dict(for_request), ensure_ascii=not ujson)

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

        def parse(val: Union['YandexMusicModel', JSONType]) -> Any:  # noqa: ANN401
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
            for k, v in data.copy().items():
                camel_case = ''.join(word.title() for word in k.split('_'))
                camel_case = camel_case[0].lower() + camel_case[1:]

                data.pop(k)
                data.update({camel_case: v})
        else:
            for k, v in data.copy().items():
                if k.lower() in reserved_names:
                    data.pop(k)
                    data.update({f'{k}_': v})

        return parse(data)

    def _get_id_attrs(self) -> Tuple[str]:
        """Получение ключевых атрибутов объекта.

        Returns:
            :obj:`tuple`: Ключевые атрибуты объекта для сравнения.
        """
        return cast(Tuple[str], getattr(self, '_id_attrs', ()))

    def __eq__(self, other: Any) -> bool:  # noqa: ANN401
        """Проверка на равенство двух объектов.

        Note:
            Проверка осуществляется по определённым атрибутам классов, перечисленных в множестве `_id_attrs`.

        Returns:
            :obj:`bool`: Одинаковые ли объекты (по содержимому).
        """
        if isinstance(other, self.__class__):
            return self._get_id_attrs() == other._get_id_attrs()
        return super(YandexMusicModel, self).__eq__(other)

    def __hash__(self) -> int:
        """Реализация хеш-функции на основе ключевых атрибутов.

        Note:
            Так как перечень ключевых атрибутов хранится в виде множества, для вычисления хеша он замораживается.

        Returns:
            :obj:`int`: Хеш объекта.
        """
        id_attrs = self._get_id_attrs()
        if not id_attrs:
            return super(YandexMusicModel, self).__hash__()

        frozen_attrs = tuple(frozenset(attr) if isinstance(attr, list) else attr for attr in id_attrs)
        return hash((self.__class__, frozen_attrs))
