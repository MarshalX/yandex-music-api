"""Операции изменения плейлиста."""

from enum import Enum
from typing import Dict, List, Union

from yandex_music.utils.json_compat import dumps as _json_dumps

TrackIdData = Dict[str, Union[str, int]]
OperationData = Dict[str, Union[str, int, List[TrackIdData]]]


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

    def __init__(self) -> None:
        self.operations: List[OperationData] = []

    def to_json(self) -> str:
        """Сериализация всех операций над плейлистом.

        Returns:
            :obj:`str`: Сформированное тело для запроса.
        """
        return _json_dumps(self.operations)

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
        operation: OperationData = {'op': Operation.DELETE.value, 'from': from_, 'to': to}

        self.operations.append(operation)
        return self

    def add_insert(self, at: int, tracks: Union[TrackIdData, List[TrackIdData]]) -> 'Difference':
        """Добавление операции вставки.

        Note:
            В `tracks` передаётся словарь с двумя ключами: `id`, `album_id`. Это нужно для формирования операции.

        Args:
            at (:obj:`int`): Индекс для вставки.
            tracks (:obj:`dict` | :obj:`list: из :obj:`dict`): Словарь уникальными идентификаторами треков.

        Returns:
            :obj:`yandex_music.utils.difference.Difference`: Набор операций над плейлистом.
        """
        # TODO (MarshalX) принимать TrackId, а так же строку и сплитить её по ":".
        #  При отсутствии album_id кидать исключение.
        #  https://github.com/MarshalX/yandex-music-api/issues/558
        if not isinstance(tracks, list):
            tracks = [tracks]

        operation_tracks: List[TrackIdData] = []
        operation: OperationData = {'op': Operation.INSERT.value, 'at': at, 'tracks': operation_tracks}

        for track in tracks:
            # TODO (MarshalX) replace to normal TrackId object
            #  https://github.com/MarshalX/yandex-music-api/issues/558
            operation_tracks.append({'id': track['id'], 'albumId': track['album_id']})

        self.operations.append(operation)
        return self
