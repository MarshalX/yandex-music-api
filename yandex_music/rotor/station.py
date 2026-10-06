from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Icon, Id, Restrictions


@model
class Station(YandexMusicModel):
    """Класс, представляющий станцию.

    Note:
        `id_for_from` обозначает предка станции, например, жанр, настроение или занятие.
        Неизвестно когда используется `id_for_from`, а когда `parent_id`.

    Attributes:
        id (:obj:`yandex_music.Id`): Уникальный идентификатор станции.
        name (:obj:`str`): Название станции.
        icon (:obj:`yandex_music.Icon`): Иконка станции.
        mts_icon (:obj:`yandex_music.Icon`): Иконка TODO.
        geocell_icon (:obj:`yandex_music.Icon` | :obj:`None`): Иконка TODO.
        id_for_from (:obj:`str`): Категория (тип) станции.
        restrictions (:obj:`yandex_music.Restrictions`): Ограничения для настроек станции старого формата.
        restrictions2 (:obj:`yandex_music.Restrictions`): Ограничения для настроек станции.
        full_image_url (:obj:`str`, optional): Ссылка на полное изображение.
        mts_full_image_url (:obj:`str`, optional): Ссылка на полную иконку.
        parent_id (:obj:`yandex_music.Id`, optional): Уникальный идентификатор станции, являющейся предком текущей.
        special_context (:obj:`bool`, optional): Является ли станция особым контекстом волны.
        listeners (:obj:`int`, optional): Количество слушателей персональной станции.
        login (:obj:`str`, optional): Логин владельца персональной станции.
        full_name (:obj:`str`, optional): Полное имя владельца персональной станции.
        display_name (:obj:`str`, optional): Отображаемое имя владельца персональной станции.
        visibility (:obj:`str`, optional): Видимость персональной станции (например, `public`).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional['Id']
    name: str
    icon: 'Icon'
    mts_icon: 'Icon'
    geocell_icon: Optional['Icon']
    id_for_from: str
    restrictions: 'Restrictions'
    restrictions2: 'Restrictions'
    full_image_url: Optional[str] = None
    mts_full_image_url: Optional[str] = None
    parent_id: Optional['Id'] = None
    special_context: Optional[bool] = None
    listeners: Optional[int] = None
    login: Optional[str] = None
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    visibility: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (
            self.id,
            self.name,
            self.icon,
            self.mts_icon,
            self.geocell_icon,
            self.id_for_from,
            self.restrictions,
            self.restrictions2,
        )
