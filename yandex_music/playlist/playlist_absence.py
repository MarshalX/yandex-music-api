from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PlaylistAbsence(YandexMusicObject):
    """Класс, представляющий причину отсутствия плейлиста.

    Attributes:
        kind (:obj:`int`): Уникальный идентификатор плейлиста.
        reason (:obj:`str`): Причина отсутствия.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    kind: int
    reason: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.kind, self.reason)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlaylistAbsence']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlaylistAbsence`: Причина отсутствия плейлиста.
        """
        if not data:
            return None

        data = super(PlaylistAbsence, cls).de_json(data, client)

        return cls(client=client, **data)
