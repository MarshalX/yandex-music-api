from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Album


class AlbumsLikes(YandexMusicObject):
    def __init__(self,
                 timestamp: str,
                 id_: Optional[int] = None,
                 album: Optional['Album'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.album = album
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.id, self.album)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AlbumsLikes']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.AlbumsLikes`: Объект класса :class:`yandex_music.AlbumsLikes`.
        """
        if not data:
            return None

        data = super(AlbumsLikes, cls).de_json(data, client)
        from yandex_music import Album
        data['album'] = Album.de_json(data.get('album'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['AlbumsLikes']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.AlbumsLikes`: Список объектов класса :class:`yandex_music.AlbumsLikes`.
        """
        if not data:
            return []

        albums_likes = list()
        for album_like in data:
            albums_likes.append(cls.de_json(album_like, client))

        return albums_likes
