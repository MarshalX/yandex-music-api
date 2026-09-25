from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class GenerativeStreamFeedback(YandexMusicModel):
    """Класс, представляющий ответ на обратную связь генеративной станции.

    Attributes:
        reload_stream (:obj:`bool`, optional): Нужно ли перезагрузить поток.
        not_paused (:obj:`bool`, optional): Воспроизводится ли поток (не на паузе).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    reload_stream: Optional[bool] = None
    not_paused: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.reload_stream, self.not_paused)
