from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Album, Pager

from yandex_music import YandexMusicObject


class ArtistAlbums(YandexMusicObject):
    """Класс представляющий страницу списка альбомов артиста.

    Attributes:
        albums (:obj:`list` из :obj:`yandex_music.Album`): Список альбомов артиста.
        pager (:obj:`yandex_music.Pager`): Объект класса :class:`yandex_music.Pager` представляющий пагинатор.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        albums (:obj:`list` из :obj:`yandex_music.Album`): Список альбомов артиста.
        pager (:obj:`yandex_music.Pager`): Объект класса :class:`yandex_music.Pager` представляющий пагинатор.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 albums: List['Album'],
                 pager: Optional['Pager'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.albums = albums
        self.pager = pager

        self.client = client
        self._id_attrs = (self.pager, self.albums)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistAlbums']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.ArtistAlbums`: Объект класса :class:`yandex_music.ArtistAlbums`.
        """
        if not data:
            return None

        data = super(ArtistAlbums, cls).de_json(data, client)
        from yandex_music import Album, Pager
        data['albums'] = Album.de_list(data.get('albums'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
