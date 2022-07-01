from typing import List, Optional, Iterator, TYPE_CHECKING

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Artist, Pager


@model
class LabelArtists(YandexMusicObject):
    """Класс, представляющий страницу списка артистов лейбла.

    Attributes:
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Список артистов лейбла.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artists: List['Artist']
    pager: Optional['Pager']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.pager, self.artists)

    def __getitem__(self, item) -> 'Artist':
        return self.albums[item]

    def __iter__(self) -> Iterator['Artist']:
        return iter(self.albums)

    def __len__(self) -> int:
        return len(self.albums)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['LabelArtists']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LabelAlbums`: Список альбомов лейбла.
        """
        if not data:
            return None

        data = super(LabelArtists, cls).de_json(data, client)
        from yandex_music import Artist, Pager

        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
