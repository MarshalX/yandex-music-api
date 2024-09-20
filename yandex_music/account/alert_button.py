from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class AlertButton(YandexMusicModel):
    """Класс, представляющий кнопку в предупреждении.

    Attributes:
        text (:obj:`str`): Текст кнопки.
        bg_color (:obj:`str`): Цвет заднего фона.
        text_color (:obj:`str`): Цвет текста.
        uri (:obj:`str`): Ссылка куда ведёт кнопка.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: str
    bg_color: str
    text_color: str
    uri: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.text, self.uri)
