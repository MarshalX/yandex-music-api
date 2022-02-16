from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Plus(YandexMusicObject):
    """Класс, представляющий `Plus` подписку.

    Attributes:
        has_plus (:obj:`bool`): Наличие.
        is_tutorial_completed (:obj:`bool`): Закончено ли руководство.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    has_plus: bool
    is_tutorial_completed: bool
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.has_plus, self.is_tutorial_completed)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Plus']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Plus`: Plus подписка.
        """
        if not data:
            return None

        data = super(Plus, cls).de_json(data, client)

        return cls(client=client, **data)
