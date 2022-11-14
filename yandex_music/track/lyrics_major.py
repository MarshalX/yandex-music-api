from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model


if TYPE_CHECKING:
    from yandex_music import Client


@model
class LyricsMajor(YandexMusicObject):
    """TODO"""

    id: int
    name: str
    pretty_name: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['LyricsMajor']:
        if not data:
            return None

        data = super(LyricsMajor, cls).de_json(data, client)

        return cls(client=client, **data)
