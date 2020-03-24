from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Cover, Ratings, Counts, Link, Track, Description, ArtistTracks, ArtistAlbums


class Artist(YandexMusicObject):
    """Класс, представляющий исполнителя.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор.
        error (:obj:`str`): Сообщение об ошибке.
        name (:obj:`str`): Название.
        cover (:obj:`yandex_music.Cover` | :obj:`None`): Обложка.
        various (:obj:`bool`): TODO.
        composer (:obj:`bool`): TODO.
        genres (:obj:`list` из :obj:`str`): Жанры.
        op_image (:obj:`str`): Ссылка на изображение обложки. Используется когда не указано поле cover.
        no_pictures_from_search: TODO.
        counts (:obj:`yandex_music.Counts` | :obj:`None`): Счётчики.
        available (:obj:`bool`): Доступен ли для прослушивания.
        ratings (:obj:`yandex_music.Ratings` | :obj:`None`): Рейтинги.
        links (:obj:`list` из :obj:`yandex_music.Link`): Ссылки на ресурсы исполнителя.
        tickets_available (:obj:`bool`): Имеются ли в продаже билеты на концерт.
        regions (:obj:`list` из :obj:`str`): Регион TODO.
        decomposed: TODO.
        popular_tracks (:obj:`list` :obj:`yandex_music.Track`): Популярные треки.
        likes_count (:obj:`int`): Количество лайков.
        full_names: TODO.
        description (:obj:`yandex_music.Description` | :obj:`None`): Описание.
        countries (:obj:`list` из :obj:`str`): Страны.
        en_wikipedia_link (:obj:`str`): Адрес страницы на wikipedia.org.
        db_aliases (:obj:`list` из :obj:`str`): Другие названия. Как правило названия на разных языках.
        aliases: TODO.
        init_date (:obj:`str`): Дата начала в формате YYYY-MM-DD или YYYY.
        end_date (:obj:`str`): Дата окончания в формате YYYY-MM-DD или YYYY.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`int`): Уникальный идентификатор.
        error (:obj:`str`, optional): Сообщение об ошибке.
        name (:obj:`str`, optional): Название.
        cover (:obj:`yandex_music.Cover`, optional): Обложка.
        various (:obj:`bool`, optional): TODO.
        composer (:obj:`bool`, optional): TODO.
        genres (:obj:`list` из :obj:`str`, optional): Жанры.
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
        decomposed: TODO.
        full_names: TODO.
        description (:obj:`yandex_music.Description`, optional): Описание.
        countries (:obj:`list` из :obj:`str`, optional): Страны.
        en_wikipedia_link (:obj:`str`, optional): Адрес страницы на wikipedia.org.
        db_aliases (:obj:`list` из :obj:`str`, optional): Другие названия. Как правило названия на разных языках.
        aliases: TODO.
        init_date (:obj:`str`, optional): Дата начала в формате YYYY-MM-DD или YYYY.
        end_date (:obj:`str`, optional): Дата окончания в формате YYYY-MM-DD или YYYY.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: int,
                 error: Optional[str] = None,
                 name: Optional[str] = None,
                 cover: Optional['Cover'] = None,
                 various: Optional[bool] = None,
                 composer: Optional[bool] = None,
                 genres: Optional[List[str]] = None,
                 op_image: Optional[str] = None,
                 no_pictures_from_search=None,
                 counts: Optional['Counts'] = None,
                 available: Optional[bool] = None,
                 ratings: Optional['Ratings'] = None,
                 links: Optional[List['Link']] = None,
                 tickets_available: Optional[bool] = None,
                 likes_count: Optional[int] = None,
                 popular_tracks: Optional[List['Track']] = None,
                 regions: Optional[List[str]] = None,
                 decomposed=None,
                 full_names=None,
                 description: Optional['Description'] = None,
                 countries: Optional[List[str]] = None,
                 en_wikipedia_link: Optional[str] = None,
                 db_aliases: Optional[List[str]] = None,
                 aliases=None,
                 init_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 client: 'Client' = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.id = id_

        self.error = error
        self.name = name
        self.cover = cover
        self.various = various
        self.composer = composer
        self.genres = genres
        self.op_image = op_image
        self.no_pictures_from_search = no_pictures_from_search
        self.counts = counts
        self.available = available
        self.ratings = ratings
        self.links = links
        self.tickets_available = tickets_available
        self.regions = regions
        self.decomposed = decomposed
        self.popular_tracks = popular_tracks
        self.likes_count = likes_count
        self.full_names = full_names
        self.description = description
        self.countries = countries
        self.en_wikipedia_link = en_wikipedia_link
        self.db_aliases = db_aliases
        self.aliases = aliases

        # Может прийти конкретная дата или просто год
        self.init_date = init_date
        self.end_date = end_date

        self.client = client
        self._id_attrs = (self.id, self.name, self.cover)

    def download_op_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.op_image.replace("%%", size)}', filename)

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_artists_add(artist.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_artists_add(self.id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_artists_remove(artist.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_artists_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    def get_tracks(self, page=0, page_size=20, *args, **kwargs) -> Optional['ArtistTracks']:
        """Сокращение для::

            client.artists_tracks(artist.id, page, page_size, *args, **kwargs)
        """
        return self.client.artists_tracks(self.id, page, page_size, *args, **kwargs)

    def get_albums(self, page=0, page_size=20, sort_by='year', *args, **kwargs) -> Optional['ArtistAlbums']:
        """Сокращение для::

            client.artists_direct_albums(artist.id, page, page_size, sort_by, *args, **kwargs)
        """
        return self.client.artists_direct_albums(self.id, page, page_size, sort_by, *args, **kwargs)

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
        # TODO add "decomposed" deserialization

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

    #: Псевдоним для :attr:`download_op_image`
    downloadOpImage = download_op_image
    #: Псевдоним для :attr:`get_tracks`
    getTracks = get_tracks
    #: Псевдоним для :attr:`get_albums`
    getAlbums = get_albums
