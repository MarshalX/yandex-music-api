from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class TrackId(YandexMusicObject):
    """Класс, представляющий уникальный идентификатор трека.

    Note:
        Поле `track_id` используется только у объектах полученных через очередь треков. В остальные случаях `id`.

        Поле `from_` есть только у объект, которые используются в очереди треков.

    Attributes:
        id_ (:obj:`int`): Уникальный идентификатор трека.
        track_id (:obj:`int`): Уникальный идентификатор трека.
        album_id (:obj:`int`): Уникальный идентификатор альбома.
        from_ (:obj:`str`): Откуда был получен этот объект.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`int`): Уникальный идентификатор трека.
        track_id (:obj:`int`): Уникальный идентификатор трека.
        album_id (:obj:`int`, optional): Уникальный идентификатор альбома.
        from_ (:obj:`str`, optional): Откуда был получен этот объект.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: Optional[int] = None,
                 track_id: Optional[int] = None,
                 album_id: Optional[int] = None,
                 from_: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.track_id = track_id
        self.album_id = album_id
        self.from_ = from_

        self.client = client
        self._id_attrs = (self.track_id, self.id, self.album_id)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackId']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackId`: Уникальный идентификатор трека.
        """
        if not data:
            return None

        data = super(TrackId, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['TrackId']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.TrackId`: Уникальные идентификаторы треков.
        """
        if not data:
            return []

        return [cls.de_json(track_id, client) for track_id in data]
