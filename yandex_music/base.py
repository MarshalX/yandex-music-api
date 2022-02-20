import dataclasses
import logging
import keyword
from abc import ABCMeta
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

ujson: bool = False
try:
    import ujson as json

    ujson = True
except ImportError:
    import json

reserved_names = keyword.kwlist

logger = logging.getLogger(__name__)
new_issue_by_template_url = 'https://bit.ly/3dsFxyH'


class YandexMusicObject:
    __metaclass__ = ABCMeta
    _id_attrs: tuple = ()

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item):
        return self.__dict__[item]

    @staticmethod
    def report_unknown_fields_callback(obj, unknown_fields):
        logger.warning(
            f'Found unknown fields received from API! Please copy warn message '
            f'and send to {new_issue_by_template_url} (github issue), thank you!'
        )
        logger.warning(f'Type: {type(obj)}; fields: {unknown_fields}')

    @classmethod
    def de_json(cls, data: dict, client: Optional['Client']) -> Optional[dict]:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.YandexMusicObject` | :obj:`None`: :obj:`yandex_music.YandexMusicObject` или :obj:`None`.
        """
        if not data:
            return None

        data = data.copy()

        fields = {f.name for f in dataclasses.fields(cls)}

        cleaned_data = dict()
        unknown_data = dict()

        for k, v in data.items():
            if k in fields:
                cleaned_data[k] = v
            else:
                unknown_data[k] = v

        if client.report_unknown_fields and unknown_data:
            YandexMusicObject.report_unknown_fields_callback(cls, unknown_data)

        return cleaned_data

    def to_json(self, for_request=False) -> str:
        """Сериализация объекта.

        Args:
            for_request (:obj:`bool`): Подготовить ли объект для отправки в теле запроса.

        Returns:
            :obj:`str`: Сериализованный в JSON объект.
        """
        return json.dumps(self.to_dict(for_request), ensure_ascii=not ujson)

    def to_dict(self, for_request=False) -> dict:
        """Рекурсивная сериализация объекта.

        Args:
            for_request (:obj:`bool`): Перевести ли обратно все поля в camelCase и игнорировать зарезервированные слова.

        Note:
            Исключает из сериализации `client` и `_id_attrs` необходимые в `__eq__`.

            К зарезервированным словам добавляет "_" в конец.

        Returns:
            :obj:`dict`: Сериализованный в dict объект.
        """

        def parse(val):
            if hasattr(val, 'to_dict'):
                return val.to_dict(for_request)
            elif isinstance(val, list):
                return [parse(it) for it in val]
            elif isinstance(val, dict):
                return {key: parse(value) for key, value in val.items()}
            else:
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

    def __eq__(self, other) -> bool:
        """Проверка на равенство двух объектов.

        Note:
            Проверка осуществляется по определённым атрибутам классов, перечисленных в множестве `_id_attrs`.

        Returns:
            :obj:`bool`: Одинаковые ли объекты (по содержимому).
        """
        if isinstance(other, self.__class__):
            return self._id_attrs == other._id_attrs
        return super(YandexMusicObject, self).__eq__(other)

    def __hash__(self) -> int:
        """Реализация хеш-функции на основе ключевых атрибутов.

        Note:
            Так как перечень ключевых атрибутов хранится в виде множества, для вычисления хеша он замораживается.

        Returns:
            :obj:`int`: Хеш объекта.
        """
        if self._id_attrs:
            frozen_attrs = tuple(frozenset(attr) if isinstance(attr, list) else attr for attr in self._id_attrs)
            return hash((self.__class__, frozen_attrs))
        return super(YandexMusicObject, self).__hash__()
