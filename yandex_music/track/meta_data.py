from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class MetaData(YandexMusicObject):
    """Класс, представляющий метаданные трека.

    Attributes:
        album (:obj:`str`): Название альбома.
        volume (:obj:`int`): Диск (раздел).
        year (:obj:`int`): Год выхода.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        album (:obj:`str`): Название альбома.
        volume (:obj:`int`): Диск (раздел).
        year (:obj:`int`): Год выхода.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 album: str,
                 volume: int,
                 year: int,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.album = album
        self.volume = volume
        self.year = year

        self.client = client
        self._id_attrs = (self.album, self.volume, self.year)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['MetaData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MetaData`: Метаданные трека
        """
        if not data:
            return None

        data = super(MetaData, cls).de_json(data, client)

        return cls(client=client, **data)
