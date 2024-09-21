from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Description(YandexMusicModel):
    """Класс, представляющий описание исполнителя из другого источника.

    Note:
        Очень редкий объект, у минимального количества исполнителей.
        Обычно берётся информация из википедии.

    Attributes:
        text (:obj:`str`): Описание исполнителя.
        uri (:obj:`str`): Ссылка на источник.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: str
    uri: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.text, self.uri)
