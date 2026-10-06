from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, GenerativeStreamData, GenerativeStreamInfo


@model
class GenerativeStream(YandexMusicModel):
    """Класс, представляющий информацию о генеративной станции.

    Note:
        Доступно только для генеративных станций, например, `generative:focus`, `generative:energy`,
        `generative:calm`, `generative:relax`.

    Attributes:
        data (:obj:`yandex_music.GenerativeStreamData`, optional): Оформление станции.
        version (:obj:`str`, optional): Версия генеративной модели.
        stream (:obj:`yandex_music.GenerativeStreamInfo`, optional): Поток станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    data: Optional['GenerativeStreamData'] = None
    version: Optional[str] = None
    stream: Optional['GenerativeStreamInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.data, self.version, self.stream)
