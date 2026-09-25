from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Wave(YandexMusicModel):
    """Класс, представляющий волну (персональную радиостанцию).

    Note:
        Известные значения поля `type`: `DEFAULT`.

    Attributes:
        name (:obj:`str`, optional): Название волны.
        description (:obj:`str`, optional): Описание волны.
        seeds (:obj:`list` из :obj:`str`, optional): Список сидов волны (например, ``album:12345``).
        station_id (:obj:`str`, optional): Идентификатор станции волны (например, ``user:onyourwave``).
        id_for_from (:obj:`str`, optional): Идентификатор волны для поля `from` в обратной связи.
        type (:obj:`str`, optional): Тип волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    seeds: Optional[List[str]] = None
    station_id: Optional[str] = None
    id_for_from: Optional[str] = None
    type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.name, self.seeds)
