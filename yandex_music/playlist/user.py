from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class User(YandexMusicModel):
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

    def __post_init__(self) -> None:
        self._id_attrs = (self.uid, self.login)
