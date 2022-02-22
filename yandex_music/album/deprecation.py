from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Deprecation(YandexMusicObject):
    """Класс, представляющий TODO.

    Attributes:
        target_album_id (:obj:`int`): Идентификатор альбома TODO.
        status (:obj:`str`): Состояние TODO.
        done (:obj:`str`): Выполнен ли TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    target_album_id: Optional[int]
    status: Optional[str]
    done: Optional[bool]
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.target_album_id, self.status, self.done)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Deprecation']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        Returns:
            :obj:`yandex_music.Deprecation`: TODO.
        """
        if not data:
            return None

        data = super(Deprecation, cls).de_json(data, client)

        return cls(client=client, **data)
