from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, CombinedSessionItem


@model
class CombinedSessionLanding(YandexMusicModel):
    """Класс, представляющий витрину комбинированной сессии радио (например, «Время клипов»).

    Attributes:
        title (:obj:`str`, optional): Заголовок.
        description (:obj:`str`, optional): Описание.
        button (:obj:`str`, optional): Текст кнопки.
        list (:obj:`list` из :obj:`yandex_music.CombinedSessionItem`, optional): Элементы витрины.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[str] = None
    list: Optional[List['CombinedSessionItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.list)
