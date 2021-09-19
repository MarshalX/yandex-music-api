from typing import TYPE_CHECKING, Optional, List, Iterator

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Album, Pager


@model
class ArtistAlbums(YandexMusicObject):
    """Класс, представляющий страницу списка альбомов артиста.

    Attributes:
        albums (:obj:`list` из :obj:`yandex_music.Album`): Список альбомов артиста.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    albums: List['Album']
    pager: Optional['Pager']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.pager, self.albums)

    def __getitem__(self, item) -> 'Album':
        return self.albums[item]

    def __iter__(self) -> Iterator['Album']:
        return iter(self.albums)

    def __len__(self) -> int:
        return len(self.albums)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistAlbums']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistAlbums`: Список альбомов артиста.
        """
        if not data:
            return None

        data = super(ArtistAlbums, cls).de_json(data, client)
        from yandex_music import Album, Pager

        data['albums'] = Album.de_list(data.get('albums'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
