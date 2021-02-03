from enum import Enum
from typing import List, Union

ujson = False
try:
    import ujson as json

    ujson = True
except ImportError:
    import json


class Operation(Enum):
    """Класс перечисления типов операций для изменения плейлиста.

    Note:
        Существует две операции: вставка, удаление.
    """

    INSERT = 'insert'
    DELETE = 'delete'


class Difference:
    """Класс, представляющий обёртку над созданием данных для запроса изменения плейлиста.

    Note:
        Результатом является перечень (массив) операций, которые будут применены к плейлисту.

        Конечной разницей (набором операций) является JSON, который будет отправлен в теле запроса.

    Attributes:
        operations (:obj:`list` из :obj:`dict`): Перечень операция для изменения плейлиста.
    """

    def __init__(self):
        self.operations = []

    def to_json(self) -> str:
        """Сериализация всех операций над плейлистом.

        Returns:
            :obj:`str`: Сформированное тело для запроса.
        """
        return json.dumps(self.operations, ensure_ascii=not ujson)

    def add_delete(self, from_: int, to: int) -> 'Difference':
        """Добавление операции удаления.

        Note:
            Передаётся диапазон для удаления треков.

        Args:
            from_ (:obj:`int`): С какого индекса.
            to (:obj:`int`): По какой индекс.

        Returns:
            :obj:`yandex_music.utils.difference.Difference`: Набор операций над плейлистом.
        """
        operation = {'op': Operation.DELETE.value, 'from': from_, 'to': to}

        self.operations.append(operation)
        return self

    def add_insert(self, at: int, tracks: Union[dict, List[dict]]) -> 'Difference':
        """Добавление операции вставки.

        Note:
            В `tracks` передаётся словарь с двумя ключами: `id`, `album_id`. Это нужно для формирования операции.

        Args:
            at (:obj:`int`): Индекс для вставки.
            tracks (:obj:`dict` | :obj:`list: из :obj:`dict`): Словарь уникальными идентификаторами треков.

        Returns:
            :obj:`yandex_music.utils.difference.Difference`: Набор операций над плейлистом.
        """
        # TODO принимать TrackId, а так же строку и сплитить её по ":". При отсутствии album_id кидать исключение.
        if not isinstance(tracks, list):
            tracks = [tracks]

        operation = {'op': Operation.INSERT.value, 'at': at, 'tracks': []}

        for track in tracks:
            track = type('TrackId', (), track)  # TODO replace to normal TrackId object

            operation['tracks'].append({'id': track.id, 'albumId': track.album_id})

        self.operations.append(operation)
        return self
