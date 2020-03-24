from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Normalization(YandexMusicObject):
    """Класс, представляющий значения для нормализации трека.

    Attributes:
        gain (:obj:`str`): Значение гейна, которое нужно применить к аудиосигналу.
        peak (:obj:`int`): Пиковая точка волны аудиосигнала.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        gain (:obj:`str`): Значение гейна, которое нужно применить к аудиосигналу.
        peak (:obj:`int`): Пиковая точка волны аудиосигнала.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 gain: float,
                 peak: int,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.gain = gain
        self.peak = peak

        self.client = client
        self._id_attrs = (self.gain, self.peak)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Normalization']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Normalization`: Значения для нормализации трека.
        """
        if not data:
            return None

        data = super(Normalization, cls).de_json(data, client)

        return cls(client=client, **data)
