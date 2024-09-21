from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class PoetryLoverMatch(YandexMusicModel):
    """Класс, представляющий слова в тексте TODO.

    Note:
        Некая разметка для обучения чего-нибудь для написания романтических стихотворений.

    Attributes:
        begin (:obj:`int`): Индекс начала.
        end (:obj:`int`): Индекс конца.
        line (:obj:`int`): Индекс строки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    begin: int
    end: int
    line: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.begin, self.end, self.line)
