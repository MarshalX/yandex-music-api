from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Artist


class ArtistsLikes(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_=None,
                 artist: Optional['Artist'] = None,
                 timestamp: str = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.artist = artist
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.id, self.artist)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistsLikes']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistsLikes`: Объект класса :class:`yandex_music.ArtistsLikes`.
        """
        if not data:
            return None

        data = super(ArtistsLikes, cls).de_json(data, client)
        from yandex_music import Artist
        if 'artist' not in data:
            temp_data = data.copy()
            data.clear()
            data['artist'] = Artist.de_json(temp_data, client)
        else:
            data['artist'] = Artist.de_json(data.get('artist'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['ArtistsLikes']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ArtistsLikes`: Список объектов класса :class:`yandex_music.ArtistsLikes`.
        """
        if not data:
            return []

        artists_likes = list()
        for artist_like in data:
            artists_likes.append(cls.de_json(artist_like, client))

        return artists_likes
