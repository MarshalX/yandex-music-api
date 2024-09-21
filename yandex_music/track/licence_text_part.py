from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class LicenceTextPart(YandexMusicModel):
    """Класс, представляющий часть текста с ссылкой на лицензионное соглашение.

    Attributes:
        text (:obj:`str`): Часть текста (строка).
        url (:obj:`str`, optional): Ссылка на лицензионное соглашение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: str
    url: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.text,)
