from typing import TYPE_CHECKING, List, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class MusicHistoryItemId(YandexMusicModel):
    """Класс, представляющий идентификатор элемента истории прослушивания.

    Note:
        Набор заполненных полей зависит от типа элемента:

        - ``album`` / ``artist``: `id`.
        - ``track``: `track_id` и `album_id`.
        - ``playlist``: `uid` и `kind`.
        - ``wave``: `seeds`.

    Attributes:
        id (:obj:`str`, optional): Идентификатор альбома или исполнителя.
        track_id (:obj:`str`, optional): Идентификатор трека.
        album_id (:obj:`str`, optional): Идентификатор альбома трека.
        uid (:obj:`int`, optional): Идентификатор владельца плейлиста.
        kind (:obj:`int`, optional): Идентификатор плейлиста.
        seeds (:obj:`list` из :obj:`str`, optional): Семена волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    track_id: Optional[str] = None
    album_id: Optional[str] = None
    uid: Optional[Union[str, int]] = None
    kind: Optional[Union[str, int]] = None
    seeds: Optional[List[str]] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.track_id, self.album_id, self.uid, self.kind, self.seeds)
