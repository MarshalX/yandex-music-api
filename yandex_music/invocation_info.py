from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class InvocationInfo(YandexMusicModel):
    """Класс, представляющий информацию о запросе.

    Attributes:
        hostname (:obj:`str`): Имя удалённого сервера.
        req_id (:obj:`str`): Номер запроса.
        exec_duration_millis (:obj:`str`, optional): Время выполнения в миллисекундах.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    hostname: str
    req_id: str
    exec_duration_millis: Optional[int] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.hostname, self.req_id)
