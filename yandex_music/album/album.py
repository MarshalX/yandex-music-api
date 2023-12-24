from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, Client, Deprecation, Label, Track, TrackPosition


@model
class Album(YandexMusicObject):
    """Класс, представляющий альбом.

    Note:
        Известные типы альбома: `single` - сингл, `compilation` - сборник.

        Известные предупреждения о содержимом: `explicit` - ненормативная лексика.

        Известные ошибки: `not-found` - альбом с таким ID не существует.

        Известные значения поля `meta_type`: `music`.

        Известные значения поля `available_for_options`: `bookmate`.

    Attributes:
        id (:obj:`int`, optional): Идентификатор альбома.
        error (:obj:`str`, optional): Ошибка получения альбома.
        title (:obj:`str`, optional): Название альбома.
        track_count (:obj:`int`, optional): Количество треков.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Артисты.
        labels (:obj:`list` из :obj:`yandex_music.Label` или :obj:`str`, optional): Лейблы.
        available (:obj:`bool`, optional): Доступен ли альбом.
        available_for_premium_users (:obj:`bool`, optional): Доступен ли альбом для пользователей с подпиской.
        version (:obj:`str`, optional): Дополнительная информация об альбоме.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        content_warning (:obj:`str`, optional): Предупреждение о содержимом альбома.
        original_release_year: TODO.
        genre (:obj:`str`, optional): Жанр музыки.
        text_color (:obj:`str`, optional): Цвет текста описания.
        short_description (:obj:`str`, optional): Короткое описание.
        description (:obj:`str`, optional): Описание.
        is_premiere (:obj:`bool`, optional): Премьера ли.
        is_banner (:obj:`bool`, optional): Является ли баннером.
        meta_type (:obj:`str`, optional): Мета тип TODO.
        storage_dir (:obj:`str`, optional): В какой папке на сервере хранится файл TODO.
        og_image (:obj:`str`, optional): Ссылка на превью Open Graph.
        recent (:obj:`bool`, optional): Является ли альбом новым.
        very_important (:obj:`bool`, optional): Популярен ли альбом у слушателей.
        available_for_mobile (:obj:`bool`, optional): Доступен ли альбом из приложения для телефона.
        available_partially (:obj:`bool`, optional): Доступен ли альбом частично для пользователей без подписки.
        bests (:obj:`list` из :obj:`int`, optional): ID лучших треков альбома.
        duplicates (:obj:`list` из :obj:`yandex_music.Album`, optional): Альбомы-дубликаты.
        prerolls (:obj:`list`, optional): Прероллы TODO.
        volumes (:obj:`list` из :obj:`list` из :obj:`Track`, optional): Треки альбома, разделённые по дискам.
        year (:obj:`int`, optional): Год релиза.
        release_date (:obj:`str`, optional): Дата релиза в формате ISO 8601.
        type (:obj:`str`, optional): Тип альбома.
        track_position (:obj:`yandex_music.TrackPosition`, optional): Позиция трека в альбоме. Возвращается при
            получении альбома в составе трека.
        regions (:obj:`list` из :obj:`str`, optional): Список регионов в которых доступен альбом.
        available_as_rbt (:obj:`bool`, optional): TODO.
        lyrics_available (:obj:`bool`, optional): Доступны ли слова TODO.
        remember_position (:obj:`bool`, optional): Запоминание позиции TODO.
        albums (:obj:`list` из :obj:`yandex_music.Album`, optional): Альбомы TODO.
        duration_ms (:obj:`int`, optional): Длительность в миллисекундах.
        explicit (:obj:`bool`, optional): Есть ли в треке ненормативная лексика.
        start_date (:obj:`str`, optional): Дата начала в формате ISO 8601 TODO.
        likes_count (:obj:`int`, optional): Количество лайков TODO.
        deprecation (:obj:`yandex_music.Deprecation`, optional): TODO.
        available_regions (:obj:`list` из :obj:`str`, optional): Регионы, где доступен альбом.
        available_for_options (:obj:`list` из :obj:`str`, optional): Возможные опции для альбома.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[int] = None
    error: Optional[str] = None
    title: Optional[str] = None
    track_count: Optional[int] = None
    artists: List['Artist'] = None
    labels: List[Union['Label', str]] = None
    available: Optional[bool] = None
    available_for_premium_users: Optional[bool] = None
    version: Optional[str] = None
    cover_uri: Optional[str] = None
    content_warning: Optional[str] = None
    original_release_year: Any = None
    genre: Optional[str] = None
    text_color: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    is_premiere: Optional[bool] = None
    is_banner: Optional[bool] = None
    meta_type: Optional[str] = None
    storage_dir: Optional[str] = None
    og_image: Optional[str] = None
    buy: Optional[list] = None
    recent: Optional[bool] = None
    very_important: Optional[bool] = None
    available_for_mobile: Optional[bool] = None
    available_partially: Optional[bool] = None
    bests: Optional[List[int]] = None
    duplicates: List['Album'] = None
    prerolls: Optional[list] = None
    volumes: Optional[List[List['Track']]] = None
    year: Optional[int] = None
    release_date: Optional[str] = None
    type: Optional[str] = None
    track_position: Optional['TrackPosition'] = None
    regions: Optional[List[str]] = None
    available_as_rbt: Optional[bool] = None
    lyrics_available: Optional[bool] = None
    remember_position: Optional[bool] = None
    albums: Optional[List['Album']] = None
    duration_ms: Optional[int] = None
    explicit: Optional[bool] = None
    start_date: Optional[str] = None
    likes_count: Optional[int] = None
    deprecation: Optional['Deprecation'] = None
    available_regions: Optional[List[str]] = None
    available_for_options: Optional[List[str]] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)

    def with_tracks(self, *args, **kwargs) -> Optional['Album']:
        """Сокращение для::

        client.albums_with_tracks(album.id, *args, **kwargs)
        """
        return self.client.albums_with_tracks(self.id, *args, **kwargs)

    async def with_tracks_async(self, *args, **kwargs) -> Optional['Album']:
        """Сокращение для::

        await client.albums_with_tracks(album.id, *args, **kwargs)
        """
        return await self.client.albums_with_tracks(self.id, *args, **kwargs)

    def get_cover_url(self, size: str = '200x200') -> str:
        """Возвращает URL обложки.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`str`: URL обложки.
        """
        return f'https://{self.cover_uri.replace("%%", size)}'

    def get_og_image_url(self, size: str = '200x200') -> str:
        """Возвращает URL OG обложки.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`str`: URL обложки.
        """
        return f'https://{self.og_image.replace("%%", size)}'

    def download_cover(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(self.get_cover_url(size), filename)

    async def download_cover_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(self.get_cover_url(size), filename)

    def download_og_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Предпочтительнее использовать `self.download_cover()`.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(self.get_og_image_url(size), filename)

    async def download_og_image_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Предпочтительнее использовать `self.download_cover_async()`.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(self.get_og_image_url(size), filename)

    def download_cover_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return self.client.request.retrieve(self.get_cover_url(size))

    async def download_cover_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return await self.client.request.retrieve(self.get_cover_url(size))

    def download_og_image_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Предпочтительнее использовать `self.download_cover()`.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return self.client.request.retrieve(self.get_og_image_url(size))

    async def download_og_image_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Предпочтительнее использовать `self.download_cover_async()`.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return await self.client.request.retrieve(self.get_og_image_url(size))

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_albums_add(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_add(self.id, self.client.me.account.uid, *args, **kwargs)

    async def like_async(self, *args, **kwargs) -> bool:
        """Сокращение для::

        await client.users_likes_albums_add(album.id, user.id *args, **kwargs)
        """
        return await self.client.users_likes_albums_add(self.id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_albums_remove(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    async def dislike_async(self, *args, **kwargs) -> bool:
        """Сокращение для::

        await client.users_likes_albums_remove(album.id, user.id *args, **kwargs)
        """
        return await self.client.users_likes_albums_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    def artists_name(self) -> List[str]:
        """Получает имена всех исполнителей.

        Returns:
              :obj:`list` из :obj:`str`: Имена исполнителей.
        """
        return [i.name for i in self.artists]

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Album']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Album`: Альбом.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(Album, cls).de_json(data, client)
        from yandex_music import Artist, Deprecation, Label, Track, TrackPosition

        data['artists'] = Artist.de_list(data.get('artists'), client)

        # В зависимости от запроса содержимое лейблов может быть списком объектом или списком строк.
        labels = data.get('labels')
        if cls.is_valid_model_data(labels, array=True):
            data['labels'] = Label.de_list(labels, client)
        elif labels and all(isinstance(item, str) for item in data):
            data['labels'] = labels
        else:
            # Поддержка формата. Все листы [] по умолчанию вместо None даже если данных нет.
            data['labels'] = []

        data['track_position'] = TrackPosition.de_json(data.get('track_position'), client)
        data['duplicates'] = Album.de_list(data.get('duplicates'), client)
        data['albums'] = Album.de_list(data.get('albums'), client)
        data['deprecation'] = Deprecation.de_json(data.get('deprecation'), client)
        if data.get('volumes'):
            data['volumes'] = [Track.de_list(i, client) for i in data['volumes']]

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['Album']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Album`: Альбомы.
        """
        if not cls.is_valid_model_data(data, array=True):
            return []

        return [cls.de_json(album, client) for album in data]

    # camelCase псевдонимы

    #: Псевдоним для :attr:`with_tracks`
    withTracks = with_tracks
    #: Псевдоним для :attr:`with_tracks_async`
    withTracksAsync = with_tracks_async
    #: Псевдоним для :attr:`get_cover_url`
    getCoverUrl = get_cover_url
    #: Псевдоним для :attr:`get_og_image_url`
    getOgImageUrl = get_og_image_url
    #: Псевдоним для :attr:`download_cover`
    downloadCover = download_cover
    #: Псевдоним для :attr:`download_cover_async`
    downloadCoverAsync = download_cover_async
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
    #: Псевдоним для :attr:`download_og_image_async`
    downloadOgImageAsync = download_og_image_async
    #: Псевдоним для :attr:`download_cover_bytes`
    downloadCoverBytes = download_cover_bytes
    #: Псевдоним для :attr:`download_cover_bytes_async`
    downloadCoverBytesAsync = download_cover_bytes_async
    #: Псевдоним для :attr:`download_og_image_bytes`
    downloadOgImageBytes = download_og_image_bytes
    #: Псевдоним для :attr:`download_og_image_bytes_async`
    downloadOgImageBytesAsync = download_og_image_bytes_async
    #: Псевдоним для :attr:`like_async`
    likeAsync = like_async
    #: Псевдоним для :attr:`dislike_async`
    dislikeAsync = dislike_async
    #: Псевдоним для :attr:`artists_name`
    artistsName = artists_name
