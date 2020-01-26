from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


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
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Normalization`: Объект класса :class:`yandex_music.Normalization`.
        """
        if not data:
            return None

        data = super(Normalization, cls).de_json(data, client)

        return cls(client=client, **data)
