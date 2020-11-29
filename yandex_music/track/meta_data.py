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
        number (:obj:`int`): Позиция в альбоме.
        genre (:obj:`str`): Жанр.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        album (:obj:`str`, optional): Название альбома.
        volume (:obj:`int`, optional): Диск (раздел).
        year (:obj:`int`, optional): Год выхода.
        number (:obj:`int`, optional): Позиция в альбоме.
        genre (:obj:`str`, optional): Жанр.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 album: Optional[str] = None,
                 volume: Optional[int] = None,
                 year: Optional[int] = None,
                 number: Optional[int] = None,
                 genre: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.album = album
        self.volume = volume
        self.year = year
        self.number = number
        self.genre = genre

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
