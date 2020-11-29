from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class TrackPosition(YandexMusicObject):
    """Класс, представляющий позицию трека.

    None:
        Позиция трека в альбоме, который возвращается при получении самого трека.

        Volume на фронте именуется как "Диск".

    Attributes:
        volume (:obj:`int`): Номер альбома.
        index (:obj:`int`): Порядковый номер трека.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        volume (:obj:`int`): Номер альбома.
        index (:obj:`int`): Порядковый номер трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 volume: int,
                 index: int,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.volume = volume
        self.index = index

        self.client = client
        self._id_attrs = (self.volume, self.index)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackPosition']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackPosition`: Позиция трека.
        """
        if not data:
            return None

        data = super(TrackPosition, cls).de_json(data, client)

        return cls(client=client, **data)
