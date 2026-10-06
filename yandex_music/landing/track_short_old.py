from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, TrackId


@model
class TrackShortOld(YandexMusicModel):
    """Класс, представляющий сокращённую версию трека.

    Note:
        Данная версия менее богата полями и найдена позже первой, поэтому была принята как за старую версию.

        Другая версия сокращённого трека: :class:`yandex_music.TrackShort`.

    Attributes:
        track_id (:obj:`yandex_music.TrackId`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track_id: Optional['TrackId']
    timestamp: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track_id,)
