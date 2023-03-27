from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject
from yandex_music.utils import model
from yandex_music.exceptions import InvalidBitrateError

if TYPE_CHECKING:
    from yandex_music import (
        Client,
        Normalization,
        Major,
        Album,
        Artist,
        Supplement,
        DownloadInfo,
        User,
        MetaData,
        PoetryLoverMatch,
        TrackLyrics,
        LyricsInfo,
        R128,
    )


@model
class Track(YandexMusicObject):
    """Класс, представляющий трек.

    Note:
        Известные значения поля `content_warning`: `explicit`.

        Известные значения поля `type`: `music`.

        Известные значения поля `track_sharing_flag`: `VIDEO_ALLOWED`, `COVER_ONLY`.

        Известные значения поля `track_source`: `OWN`, `OWN_REPLACED_TO_UGC`.

        Известные значения поля `available_for_options`: `bookmate`.

        Поля `can_publish`, `state`, `desired_visibility`, `filename`, `user_info` доступны только у треков что были
        загружены пользователем.

        Обычно у подкастов поле `remember_position == True`, а у треков `remember_position == False`.

        Полное описание можно получить используя :func:`Track.get_supplement`.

    Attributes:
        id (:obj:`int` | :obj:`str`): Уникальный идентификатор.
        title (:obj:`str`, optional): Название.
        available (:obj:`bool`, optional): Доступен ли для прослушивания.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Исполнители.
        albums (:obj:`list` из :obj:`yandex_music.Album`, optional): Альбомы.
        available_for_premium_users (:obj:`bool`, optional): Доступен ли для пользователей с подпиской.
        lyrics_available (:obj:`bool`, optional): Доступен ли текст песни.
        poetry_lover_matches (:obj:`list` из :obj:`yandex_music.PoetryLoverMatch`, optional): Список слов TODO.
        best (:obj:`bool`, optional): Лучшей ли трек TODO.
        real_id (:obj:`int` | :obj:`str`, optional): TODO.
        og_image (:obj:`str`, optional): Ссылка на превью Open Graph.
        type (:obj:`str`, optional): Тип.
        cover_uri (:obj:`str`, optional): Ссылка на изображение с обложкой.
        major (:obj:`yandex_music.Major`, optional): Мейджор-лейбл.
        duration_ms (:obj:`int`, optional): Длительность трека в миллисекундах.
        storage_dir (:obj:`str`, optional): В какой папке на сервере хранится файл TODO.
        file_size (:obj:`int`, optional): Размер файла. TODO добавить единицу измерения.
        substituted (:obj:`yandex_music.Track`, optional): Замещённый трек.
        matched_track (:obj:`yandex_music.Track`, optional): Соответствующий трек TODO.
        normalization (:obj:`list` из :obj:`yandex_music.Normalization`, optional): Значения для нормализации трека.
        error (:obj:`str`, optional): Сообщение об ошибке.
        can_publish (:obj:`bool`, optional): Может ли быть опубликован.
        state (:obj:`str`, optional): Состояние, например, playable.
        desired_visibility (:obj:`str`, optional): Видимость трека.
        filename (:obj:`str`, optional): Название файла.
        user_info (:obj:`yandex_music.User`, optional): Информация о пользователе, который загрузил трек.
        meta_data (:obj:`yandex_music.MetaData`, optional): Информация о метаданных трека.
        regions (:obj:`list` из :obj:`str`, optional): Регион TODO.
        available_as_rbt (:obj:`bool`, optional): TODO.
        content_warning (:obj:`str`, optional): Тип откровенного контента.
        explicit (:obj:`bool`, optional): Содержит ли откровенный контент.
        preview_duration_ms (:obj:`int`, optional): TODO.
        available_full_without_permission (:obj:`bool`, optional): Доступен ли без подписки.
        version (:obj:`str`, optional): Версия.
        remember_position (:obj:`bool`, optional): Если :obj:`True`, то запоминается последняя позиция прослушивания,
            иначе позиция не запоминается.
        background_video_uri (:obj:`str`, optional): Ссылка на видеошот.
        short_description (:obj:`str`, optional): Краткое описание эпизода подкаста.
        is_suitable_for_children (:obj:`bool`, optional): Подходит ли для детей TODO.
        track_source (:obj:`str`, optional): Источник трека.
        available_for_options (:obj:`list` из :obj:`str`, optional): Возможные опции для трека.
        r128 (:obj:`yandex_music.R128`, optional): Параметры нормализации громкости трека
            в соответствии с рекомендацией EBU R 128.
        lyrics_info (:obj:`yandex_music.LyricsInfo`, optional): Данные о наличии текстов трека.
        track_sharing_flag (:obj:`str`, optional): TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
    """

    id: Union[str, int]
    title: Optional[str] = None
    available: Optional[bool] = None
    artists: List['Artist'] = None
    albums: List['Album'] = None
    available_for_premium_users: Optional[bool] = None
    lyrics_available: Optional[bool] = None
    poetry_lover_matches: List['PoetryLoverMatch'] = None
    best: Optional[bool] = None
    real_id: Optional[Union[str, int]] = None
    og_image: Optional[str] = None
    type: Optional[str] = None
    cover_uri: Optional[str] = None
    major: Optional['Major'] = None
    duration_ms: Optional[int] = None
    storage_dir: Optional[str] = None
    file_size: Optional[int] = None
    substituted: Optional['Track'] = None
    matched_track: Optional['Track'] = None
    normalization: Optional['Normalization'] = None
    error: Optional[str] = None
    can_publish: Optional[bool] = None
    state: Optional[str] = None
    desired_visibility: Optional[str] = None
    filename: Optional[str] = None
    user_info: Optional['User'] = None
    meta_data: Optional['MetaData'] = None
    regions: Optional[List[str]] = None
    available_as_rbt: Optional[bool] = None
    content_warning: Optional[str] = None
    explicit: Optional[bool] = None
    preview_duration_ms: Optional[int] = None
    available_full_without_permission: Optional[bool] = None
    version: Optional[str] = None
    remember_position: Optional[bool] = None
    background_video_uri: Optional[str] = None
    short_description: Optional[str] = None
    is_suitable_for_children: Optional[bool] = None
    track_source: Optional[str] = None
    available_for_options: Optional[List[str]] = None
    r128: Optional['R128'] = None
    lyrics_info: Optional['LyricsInfo'] = None
    track_sharing_flag: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self.download_info = None
        self._id_attrs = (self.id,)

    def get_download_info(self, get_direct_links=False) -> List['DownloadInfo']:
        """Сокращение для::

        client.tracks_download_info(self.track_id, get_direct_links)
        """
        self.download_info = self.client.tracks_download_info(self.track_id, get_direct_links)

        return self.download_info

    async def get_download_info_async(self, get_direct_links=False) -> List['DownloadInfo']:
        """Сокращение для::

        await client.tracks_download_info(self.track_id, get_direct_links)
        """
        self.download_info = await self.client.tracks_download_info(self.track_id, get_direct_links)

        return self.download_info

    def get_supplement(self, *args, **kwargs) -> Optional['Supplement']:
        """Сокращение для::

        client.track_supplement(track.id, *args, **kwargs)
        """
        return self.client.track_supplement(self.id, *args, **kwargs)

    async def get_supplement_async(self, *args, **kwargs) -> Optional['Supplement']:
        """Сокращение для::

        await client.track_supplement(track.id, *args, **kwargs)
        """
        return await self.client.track_supplement(self.id, *args, **kwargs)

    def get_lyrics(self, *args, **kwargs) -> Optional['TrackLyrics']:
        """Сокращение для::

        client.tracks_lyrics(track.id, *args, **kwargs)
        """
        return self.client.tracks_lyrics(self.id, *args, **kwargs)

    async def get_lyrics_async(self, *args, **kwargs) -> Optional['TrackLyrics']:
        """Сокращение для::

        client.tracks_lyrics(track.id, *args, **kwargs)
        """
        return await self.client.tracks_lyrics(self.id, *args, **kwargs)

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

    def get_specific_download_info(self, codec: str, bitrate_in_kbps: int) -> Optional['DownloadInfo']:
        """Возвращает вариант загрузки по критериям.

        Args:
            codec (:obj:`str`, optional): Кодек из доступных в `self.download_info`.
            bitrate_in_kbps (:obj:`int`, optional): Битрейт из доступных в `self.download_info` для данного кодека.

        Returns:
            :obj:`yandex_music.DownloadInfo` | :obj:`None`: Вариант загрузки трека или :obj:`None`.
        """
        if self.download_info is None:
            self.get_download_info()

        for info in self.download_info:
            if info.codec == codec and info.bitrate_in_kbps == bitrate_in_kbps:
                return info
        return None

    async def get_specific_download_info_async(self, codec: str, bitrate_in_kbps: int) -> Optional['DownloadInfo']:
        """Возвращает вариант загрузки по критериям.

        Args:
            codec (:obj:`str`, optional): Кодек из доступных в `self.download_info`.
            bitrate_in_kbps (:obj:`int`, optional): Битрейт из доступных в `self.download_info` для данного кодека.

        Returns:
            :obj:`yandex_music.DownloadInfo` | :obj:`None`: Вариант загрузки трека или :obj:`None`.
        """
        if self.download_info is None:
            await self.get_download_info_async()

        for info in self.download_info:
            if info.codec == codec and info.bitrate_in_kbps == bitrate_in_kbps:
                return info
        return None

    def download(self, filename: str, codec: str = 'mp3', bitrate_in_kbps: int = 192) -> None:
        """Загрузка трека.

        Note:
            Известные значения `codec`: `mp3`, `aac`.

            Известные значения `bitrate_in_kbps`: `64`, `128`, `192`, `320`.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            codec (:obj:`str`, optional): Кодек из доступных в `self.download_info`.
            bitrate_in_kbps (:obj:`int`, optional): Битрейт из доступных в `self.download_info` для данного кодека.

        Raises:
            :class:`yandex_music.exceptions.InvalidBitrateError`: Если в `self.download_info` не найден подходящий трек.
        """
        info = self.get_specific_download_info(codec, bitrate_in_kbps)
        if info:
            info.download(filename)
        else:
            raise InvalidBitrateError('Unavailable bitrate')

    async def download_async(self, filename: str, codec: str = 'mp3', bitrate_in_kbps: int = 192) -> None:
        """Загрузка трека.

        Note:
            Известные значения `codec`: `mp3`, `aac`.

            Известные значения `bitrate_in_kbps`: `64`, `128`, `192`, `320`.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            codec (:obj:`str`, optional): Кодек из доступных в `self.download_info`.
            bitrate_in_kbps (:obj:`int`, optional): Битрейт из доступных в `self.download_info` для данного кодека.

        Raises:
            :class:`yandex_music.exceptions.InvalidBitrateError`: Если в `self.download_info` не найден подходящий трек.
        """
        info = await self.get_specific_download_info_async(codec, bitrate_in_kbps)
        if info:
            await info.download_async(filename)
        else:
            raise InvalidBitrateError('Unavailable bitrate')

    def download_bytes(self, codec: str = 'mp3', bitrate_in_kbps: int = 192) -> bytes:
        """Загрузка трека и возврат в виде байтов.

        Note:
            Известные значения `codec`: `mp3`, `aac`.

            Известные значения `bitrate_in_kbps`: `64`, `128`, `192`, `320`.

        Args:
            codec (:obj:`str`, optional): Кодек из доступных в `self.download_info`.
            bitrate_in_kbps (:obj:`int`, optional): Битрейт из доступных в `self.download_info` для данного кодека.

        Raises:
            :class:`yandex_music.exceptions.InvalidBitrateError`: Если в `self.download_info` не найден подходящий трек.

        Returns:
            :obj:`bytes`: Трек в виде байтов.
        """
        info = self.get_specific_download_info(codec, bitrate_in_kbps)
        if info:
            return info.download_bytes()
        else:
            raise InvalidBitrateError('Unavailable bitrate')

    async def download_bytes_async(self, codec: str = 'mp3', bitrate_in_kbps: int = 192) -> bytes:
        """Загрузка трека и возврат в виде байтов.

        Note:
            Известные значения `codec`: `mp3`, `aac`.

            Известные значения `bitrate_in_kbps`: `64`, `128`, `192`, `320`.

        Args:
            codec (:obj:`str`, optional): Кодек из доступных в `self.download_info`.
            bitrate_in_kbps (:obj:`int`, optional): Битрейт из доступных в `self.download_info` для данного кодека.

        Raises:
            :class:`yandex_music.exceptions.InvalidBitrateError`: Если в `self.download_info` не найден подходящий трек.

        Returns:
            :obj:`bytes`: Трек в виде байтов.
        """
        info = await self.get_specific_download_info_async(codec, bitrate_in_kbps)
        if info:
            return await info.download_bytes_async()
        else:
            raise InvalidBitrateError('Unavailable bitrate')

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_tracks_add(track.id, user.id, *args, **kwargs)
        """
        return self.client.users_likes_tracks_add(self.track_id, self.client.me.account.uid, *args, **kwargs)

    async def like_async(self, *args, **kwargs) -> bool:
        """Сокращение для::

        await client.users_likes_tracks_add(track.id, user.id, *args, **kwargs)
        """
        return await self.client.users_likes_tracks_add(self.track_id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_tracks_remove(track.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_tracks_remove(self.track_id, self.client.me.account.uid, *args, **kwargs)

    async def dislike_async(self, *args, **kwargs) -> bool:
        """Сокращение для::

        await client.users_likes_tracks_remove(track.id, user.id *args, **kwargs)
        """
        return await self.client.users_likes_tracks_remove(self.track_id, self.client.me.account.uid, *args, **kwargs)

    def artists_name(self) -> List[str]:
        """Получает имена всех исполнителей.

        Returns:
              :obj:`list` из :obj:`str`: Имена исполнителей.
        """

        return [i.name for i in self.artists]

    @property
    def track_id(self) -> str:
        """:obj:`str`: Уникальный идентификатор трека состоящий из его номера и номера альбома или просто из номера."""
        if self.albums:
            return f'{self.id}:{self.albums[0].id}'
        return f'{self.id}'

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Track']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Track`: Трек.
        """
        if not data:
            return None

        data = super(Track, cls).de_json(data, client)
        from yandex_music import Normalization, Major, Album, Artist, User, MetaData, PoetryLoverMatch, R128, LyricsInfo

        data['albums'] = Album.de_list(data.get('albums'), client)
        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['normalization'] = Normalization.de_json(data.get('normalization'), client)
        data['major'] = Major.de_json(data.get('major'), client)
        data['substituted'] = Track.de_json(data.get('substituted'), client)
        data['matched_track'] = Track.de_json(data.get('matched_track'), client)
        data['user_info'] = User.de_json(data.get('user_info'), client)
        data['meta_data'] = MetaData.de_json(data.get('meta_data'), client)
        data['poetry_lover_matches'] = PoetryLoverMatch.de_list(data.get('poetry_lover_matches'), client)
        data['r128'] = R128.de_json(data.get('r128'), client)
        data['lyrics_info'] = LyricsInfo.de_json(data.get('lyrics_info'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Track']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Track`: Треки.
        """
        if not data:
            return []

        return [cls.de_json(track, client) for track in data]

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_download_info`
    getDownloadInfo = get_download_info
    #: Псевдоним для :attr:`get_download_info_async`
    getDownloadInfoAsync = get_download_info_async
    #: Псевдоним для :attr:`get_supplement`
    getSupplement = get_supplement
    #: Псевдоним для :attr:`get_supplement_async`
    getSupplementAsync = get_supplement_async
    #: Псевдоним для :attr:`get_lyrics`
    getLyrics = get_lyrics
    #: Псевдоним для :attr:`get_lyrics_async`
    getLyricsAsync = get_lyrics_async
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
    #: Псевдоним для :attr:`get_specific_download_info`
    getSpecificDownloadInfo = get_specific_download_info
    #: Псевдоним для :attr:`get_specific_download_info_async`
    getSpecificDownloadInfoAsync = get_specific_download_info_async
    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
    #: Псевдоним для :attr:`download_bytes`
    downloadBytes = download_bytes
    #: Псевдоним для :attr:`download_bytes_async`
    downloadBytesAsync = download_bytes_async
    #: Псевдоним для :attr:`like_async`
    likeAsync = like_async
    #: Псевдоним для :attr:`dislike_async`
    dislikeAsync = dislike_async
    #: Псевдоним для :attr:`artists_name`
    artistsName = artists_name
    #: Псевдоним для :attr:`track_id`
    trackId = track_id
