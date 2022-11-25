from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class r128(YandexMusicObject):
    """Класс, описывающий свойства трека.

    Note:

    Attributes:
        i (:obj:`float`): TODO.
        tp (:obj:`float`): TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
    """

    i: float
    tp: float
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.i, self.tp)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['r128']:
        """TODO.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.r128`: TODO.
        """
        if not data:
            return None

        data = super(r128, cls).de_json(data, client)

        return cls(client=client, **data)
