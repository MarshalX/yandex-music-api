from typing import Any, TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class CustomWave(YandexMusicObject):
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

    def __post_init__(self):
        self._id_attrs = (self.title, self.animation_url, self.position)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['CustomWave']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.CustomWave`: Описание плейлиста.
        """
        if not data:
            return None

        data = super(CustomWave, cls).de_json(data, client)

        return cls(client=client, **data)
