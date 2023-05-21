from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model


if TYPE_CHECKING:
    from yandex_music import Client


@model
class LyricsMajor(YandexMusicObject):
    """Класс, представляющий сервис-источник текстов к трекам.

    Args:
        id (:obj:`int`): Уникальный идентификатор сервиса.
        name (:obj:`str`): Имя сервиса.
        pretty_name (:obj:`str`): Человекочитаемое имя сервиса.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    pretty_name: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['LyricsMajor']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LyricsMajor`: Сервис-источник текстов к трекам.
        """
        if not data:
            return None

        data = super(LyricsMajor, cls).de_json(data, client)

        return cls(client=client, **data)
