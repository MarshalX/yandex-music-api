from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, ShotData


@model
class Shot(YandexMusicModel):
    """Класс, представляющий шот от Алисы.

    Note:
        Известные значения поля `status`: `ready`.

    Attributes:
        order (:obj:`int`): Порядковый номер при воспроизведении.
        played (:obj:`bool`): Был ли проигран шот.
        shot_data (:obj:`yandex_music.ShotData`): Основная информация о шоте.
        shot_id (:obj:`str`): Уникальный идентификатор шота.
        status (:obj:`str`): Статус шота.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    order: int
    played: bool
    shot_data: 'ShotData'
    shot_id: str
    status: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.order, self.played, self.shot_data, self.shot_id, self.status)
