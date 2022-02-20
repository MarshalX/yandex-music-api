from typing import Any, TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Cover, Ratings, Counts, Link, Track, Description, ArtistTracks, ArtistAlbums


@model
class Artist(YandexMusicObject):
    """Класс, представляющий исполнителя.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор.
        error (:obj:`str`, optional): Сообщение об ошибке с объяснением почему не вернуло исполнителя.
        reason (:obj:`str`, optional): Причина отсутствия исполнителя (сообщение об ошибке).
        name (:obj:`str`, optional): Название.
        cover (:obj:`yandex_music.Cover`, optional): Обложка.
        various (:obj:`bool`, optional): TODO.
        composer (:obj:`bool`, optional): TODO.
        genres (:obj:`list` из :obj:`str`, optional): Жанры.
        og_image (:obj:`str`, optional): Ссылка на изображение для Open Graph.
        op_image (:obj:`str`, optional): Ссылка на изображение обложки. Используется когда не указано поле cover.
        no_pictures_from_search: TODO.
        counts (:obj:`yandex_music.Counts`, optional): Счётчики.
        available (:obj:`bool`, optional): Доступен ли для прослушивания.
        ratings (:obj:`yandex_music.Ratings`, optional): Рейтинги.
        links (:obj:`list` из :obj:`yandex_music.Link`, optional): Ссылки на ресурсы исполнителя.
        tickets_available (:obj:`bool`, optional): Имеются ли в продаже билеты на концерт.
        likes_count (:obj:`int`, optional): Количество лайков.
        popular_tracks (:obj:`list` :obj:`yandex_music.Track`, optional): Популярные треки.
        regions (:obj:`list` из :obj:`str`, optional): Регион TODO.
        decomposed (:obj:`list` из :obj:`str` и :obj:`yandex_music.Artist`, optional): Декомпозиция всех исполнителей.
            Лист, где чередуется разделитель и артист. Фиты и прочее.
        full_names: TODO.
        hand_made_description (:obj:`str`, optional): Описание от Яндекс TODO.
        description (:obj:`yandex_music.Description`, optional): Описание.
        countries (:obj:`list` из :obj:`str`, optional): Страны.
        en_wikipedia_link (:obj:`str`, optional): Адрес страницы на wikipedia.org.
        db_aliases (:obj:`list` из :obj:`str`, optional): Другие названия. Как правило названия на разных языках.
        aliases: TODO.
        init_date (:obj:`str`, optional): Дата начала в формате YYYY-MM-DD или YYYY.
        end_date (:obj:`str`, optional): Дата окончания в формате YYYY-MM-DD или YYYY.
        ya_money_id (:obj:`str`): Номер кошеляка Яндекс.Деньги TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
    """

    id: int
    error: Optional[str] = None
    reason: Optional[str] = None
    name: Optional[str] = None
    cover: Optional['Cover'] = None
    various: Optional[bool] = None
    composer: Optional[bool] = None
    genres: Optional[List[str]] = None
    og_image: Optional[str] = None
    op_image: Optional[str] = None
    no_pictures_from_search: Any = None
    counts: Optional['Counts'] = None
    available: Optional[bool] = None
    ratings: Optional['Ratings'] = None
    links: Optional[List['Link']] = None
    tickets_available: Optional[bool] = None
    likes_count: Optional[int] = None
    popular_tracks: Optional[List['Track']] = None
    regions: Optional[List[str]] = None
    decomposed: Optional[List[Union[str, 'Artist']]] = None
    full_names: Any = None
    hand_made_description: Optional[str] = None
    description: Optional['Description'] = None
    countries: Optional[List[str]] = None
    en_wikipedia_link: Optional[str] = None
    db_aliases: Optional[List[str]] = None
    aliases: Any = None
    init_date: Optional[str] = None
    end_date: Optional[str] = None
    ya_money_id: Optional[str] = None
    client: 'Client' = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.name, self.cover)

    def download_og_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка изображения для Open Graph.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

    async def download_og_image_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка изображения для Open Graph.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

    def download_op_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Notes:
            Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.op_image.replace("%%", size)}', filename)

    async def download_op_image_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Notes:
            Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(f'https://{self.op_image.replace("%%", size)}', filename)

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_artists_add(artist.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_artists_add(self.id, self.client.me.account.uid, *args, **kwargs)

    async def like_async(self, *args, **kwargs) -> bool:
        """Сокращение для::

        await client.users_likes_artists_add(artist.id, user.id *args, **kwargs)
        """
        return await self.client.users_likes_artists_add(self.id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_artists_remove(artist.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_artists_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    async def dislike_async(self, *args, **kwargs) -> bool:
        """Сокращение для::

        await client.users_likes_artists_remove(artist.id, user.id *args, **kwargs)
        """
        return await self.client.users_likes_artists_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    def get_tracks(self, page=0, page_size=20, *args, **kwargs) -> Optional['ArtistTracks']:
        """Сокращение для::

        client.artists_tracks(artist.id, page, page_size, *args, **kwargs)
        """
        return self.client.artists_tracks(self.id, page, page_size, *args, **kwargs)

    async def get_tracks_async(self, page=0, page_size=20, *args, **kwargs) -> Optional['ArtistTracks']:
        """Сокращение для::

        await client.artists_tracks(artist.id, page, page_size, *args, **kwargs)
        """
        return await self.client.artists_tracks(self.id, page, page_size, *args, **kwargs)

    def get_albums(self, page=0, page_size=20, sort_by='year', *args, **kwargs) -> Optional['ArtistAlbums']:
        """Сокращение для::

        client.artists_direct_albums(artist.id, page, page_size, sort_by, *args, **kwargs)
        """
        return self.client.artists_direct_albums(self.id, page, page_size, sort_by, *args, **kwargs)

    async def get_albums_async(self, page=0, page_size=20, sort_by='year', *args, **kwargs) -> Optional['ArtistAlbums']:
        """Сокращение для::

        await client.artists_direct_albums(artist.id, page, page_size, sort_by, *args, **kwargs)
        """
        return await self.client.artists_direct_albums(self.id, page, page_size, sort_by, *args, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Artist']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Artist`: Исполнитель.
        """
        if not data:
            return None

        data = super(Artist, cls).de_json(data, client)
        from yandex_music import Cover, Ratings, Counts, Link, Track, Description

        data['cover'] = Cover.de_json(data.get('cover'), client)
        data['ratings'] = Ratings.de_json(data.get('ratings'), client)
        data['counts'] = Counts.de_json(data.get('counts'), client)
        data['links'] = Link.de_list(data.get('links'), client)
        data['popular_tracks'] = Track.de_list(data.get('popular_tracks'), client)
        data['description'] = Description.de_json(data.get('description'), client)

        # Мне очень интересно увидеть как в яндухе на клиентах солвят свой бэковский костыль, пригласите на экскурсию
        if data.get('decomposed'):
            data['decomposed'] = [
                Artist.de_json(part, client) if isinstance(part, dict) else part for part in data['decomposed']
            ]

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Artist']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Artist`: Исполнители.
        """
        if not data:
            return []

        artists = list()
        for artist in data:
            artists.append(cls.de_json(artist, client))

        return artists

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
    #: Псевдоним для :attr:`download_og_image_async`
    downloadOgImageAsync = download_og_image_async
    #: Псевдоним для :attr:`download_op_image`
    downloadOpImage = download_op_image
    #: Псевдоним для :attr:`download_op_image_async`
    downloadOpImageAsync = download_op_image_async
    #: Псевдоним для :attr:`get_tracks`
    getTracks = get_tracks
    #: Псевдоним для :attr:`get_tracks_async`
    getTracksAsync = get_tracks_async
    #: Псевдоним для :attr:`get_albums`
    getAlbums = get_albums
    #: Псевдоним для :attr:`get_albums_async`
    getAlbumsAsync = get_albums_async
    #: Псевдоним для :attr:`like_async`
    likeAsync = like_async
    #: Псевдоним для :attr:`dislike_async`
    dislikeAsync = dislike_async
