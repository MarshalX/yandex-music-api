import logging
from typing import Dict, Optional, Union

from typing_extensions import TypeGuard

from yandex_music import Album, Artist, JSONType, Playlist, Status, Track, YandexMusicObject

de_list = {
    'artist': Artist.de_list,
    'album': Album.de_list,
    'track': Track.de_list,
    'playlist': Playlist.de_list,
}

logging.getLogger(__name__).addHandler(logging.NullHandler())

UserIdType = Optional[Union[str, int]]
TimestampType = Optional[Union[str, float, int]]


def is_dict(data: Optional[JSONType]) -> TypeGuard[Dict[str, JSONType]]:
    """TypeGuard для сужения JSONType до словаря."""
    return isinstance(data, dict)


class ClientBase(YandexMusicObject):
    """Базовый класс клиента с объявлениями общих атрибутов.

    Предоставляет аннотации типов для атрибутов, общих между синхронным и асинхронным клиентами.
    Используется как базовый класс для миксинов, чтобы средства проверки типов видели общие атрибуты.
    """

    logger: logging.Logger
    token: Optional[str]
    base_url: str
    report_unknown_fields: bool
    language: str
    device: str
    me: Optional[Status] = None
    account_uid: Optional[int] = None
