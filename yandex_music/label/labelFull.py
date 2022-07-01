from typing import Optional, Union, List, TYPE_CHECKING

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Link


@model
class LabelFull(YandexMusicObject):
    """Класс, представляющий лейбл.

    Attributes:
        id (:obj:`int` | :obj:`str`): Уникальный идентификатор.
        name (:obj:`str`): Название.
        description (:obj:`str`, optional): описание.
        descriptionFormatted (:obj:`str`, optional): Описание лейбла. Только текст, без разметки.
        image (:obj:`str`, optional): ссылка на изобржение.
        links (:obj:`list` из :obj:`yandex_music.Link`, optional): Ссылки на ресурсы исполнителя.
        type (:obj:`str`, optional): тип лейбла.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
    """

    id: Union[str, int]
    name: Optional[str] = None
    description: Optional[str] = None
    description_formatted: Optional[str] = None
    image: Optional[str] = None
    links: Optional[List['Link']] = None
    type: Optional[str] = None
    client: Optional['Client'] = None

    def get_artists(self, page: Union[int] = 0):
        """Сокращение для::

        client.get_label_artists(self.label_id, page)
        """

        return self.client.get_label_artists(self.id, page)

    def get_albums(self, page: Union[int] = 0):
        """Сокращение для::

        client.get_label_albums(self.label_id, page)
        """
        return self.client.get_label_albums(self.id, page)

    async def get_artists_async(self, page: Union[int] = 0):
        """Сокращение для::

        await client.get_label_artists(self.label_id, page)
        """

        return await self.client.get_label_artists(self.id, page)

    async def get_albums_async(self, page: Union[int] = 0):
        """Сокращение для::

        await client.get_label_albums(self.label_id, page)
        """
        return await self.client.get_label_albums(self.id, page)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['LabelFull']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LabelFull`: Label.
        """

        if not data:
            return None

        data = super(LabelFull, cls).de_json(data, client)
        from yandex_music import Link

        data['links'] = Link.de_list(data.get('links'), client)
        data['type'] = data.get('type')

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_artists`
    getArtists = get_artists
    #: Псевдоним для :attr:`get_artists_async`
    getArtistsAsync = get_artists_async
    #: Псевдоним для :attr:`get_albums`
    getAlbums = get_albums
    #: Псевдоним для :attr:`get_albums_async`
    getAlbumsAsync = get_albums_async
