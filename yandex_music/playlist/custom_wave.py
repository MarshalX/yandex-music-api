from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class CustomWave(YandexMusicModel):
    """Класс, представляющий дополнительное описание плейлиста.

    Note:
        Известные значения `position`: `default`.

    Attributes:
        title (:obj:`str`): Название плейлиста.
        animation_url (:obj:`str`): JSON анимация Lottie.
        position (:obj:`str`): Позиция TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    animation_url: str
    position: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.animation_url, self.position)
