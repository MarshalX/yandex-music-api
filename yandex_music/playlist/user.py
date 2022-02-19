from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class User(YandexMusicObject):
    """Класс, представляющий пользователя.

    Note:
        Когда данный класс используется в `MadeFor` и `Playlist, то доступны все поля кроме `display_name` и
        `full_name`.

        При наличии экземпляра класса в `user_info` у `Track` (у самозагруженных треков) доступны только `uid`,
        '`login`, 'display_name` и `full_name`.

        Поле `regions` есть только при возвращении пользователей в результатах поисках.

    Attributes:
        uid (:obj:`int`): Идентификатор пользователя.
        login (:obj:`str`): Логин пользователя.
        name (:obj:`str`, optional): Имя пользователя.
        display_name (:obj:`str`, optional): Отображаемое пользователя.
        full_name (:obj:`str`, optional): Полное имя пользователя.
        sex (:obj:`str`, optional): Пол пользователя.
        verified (:obj:`bool`, optional): Участвует ли пользователь в генерации плейлистов дня и т.д., и т.п.
        regions (:obj:`list` из :obj:`int`, optional): Список регионов TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    uid: int
    login: str
    name: Optional[str] = None
    display_name: Optional[str] = None
    full_name: Optional[str] = None
    sex: Optional[str] = None
    verified: Optional[bool] = None
    regions: List[int] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.uid, self.login)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['User']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.User`: Пользователь.
        """
        if not data:
            return None

        data = super(User, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['User']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.User`: Пользователи.
        """
        if not data:
            return []

        return [cls.de_json(user, client) for user in data]
