from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Normalization(YandexMusicObject):
    def __init__(self,
                 gain: float,
                 peak: int,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.gain = gain
        self.peak = peak

        self.client = client
        self._id_attrs = (self.gain, self.peak)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Normalization']:
        if not data:
            return None

        data = super(Normalization, cls).de_json(data, client)

        return cls(client=client, **data)
