from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject
from yandex_music.exceptions import InvalidBitrate

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
    )


class Track(YandexMusicObject):
    """Класс, представляющий трек.

    Note:
        Известные значения поля `content_warning`: `explicit`.

        Известные значения поля `type`: `music`.

        Поля `can_publish`, `state`, `desired_visibility`, `filename`, `user_info` доступны только у треков что были
        загружены пользователем.

        Обычно у подкастов поле `remember_position == True`, а у треков `remember_position == False`.

        Полное описание можно получить используя :func:`Track.get_supplement`.

    Attributes:
        id (:obj:`int` | :obj:`str`): Уникальный идентификатор.
        title (:obj:`str`): Название.
        available (:obj:`bool`): Доступен ли для прослушивания.
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Исполнители.
        albums (:obj:`list` из :obj:`yandex_music.Album`): Альбомы.
        available_for_premium_users (:obj:`bool`): Доступен ли для пользователей с подпиской.
        lyrics_available (:obj:`bool`): Доступен ли текст песни.
        poetry_lover_matches (:obj:`list` из :obj:`yandex_music.PoetryLoverMatch`): Список слов TODO.
        best (:obj:`bool`): Лучшей ли трек TODO.
        real_id (:obj:`int` | :obj:`str`): TODO.
        og_image (:obj:`str`): Ссылка на превью Open Graph.
        type (:obj:`str`): Тип.
        cover_uri (:obj:`str`): Ссылка на изображение с обложкой.
        major (:obj:`yandex_music.Major` | :obj:`None`): Мейджор-лейбл.
        duration_ms (:obj:`int`): Длительность трека в миллисекундах.
        storage_dir (:obj:`str`): В какой папке на сервере хранится файл TODO.
        file_size (:obj:`int`):  Размер файла. TODO добавить единицу измерения.
        substituted (:obj:`yandex_music.Track`): Замещённый трек.
        matched_track (:obj:`yandex_music.Track`): Соответствующий трек TODO.
        normalization (:obj:`list` из :obj:`yandex_music.Normalization`): Значения для нормализации трека.
        error (:obj:`str`): Сообщение об ошибке.
        can_publish (:obj:`bool`): Может ли быть опубликован.
        state (:obj:`str`): Состояние, например, playable.
        desired_visibility (:obj:`str`): Видимость трека.
        filename (:obj:`str`): Название файла.
        user_info (:obj:`yandex_music.User`): Информация о пользователе, который загрузил трек.
        meta_data (:obj:`yandex_music.MetaData`): Информация о метаданных трека.
        regions (:obj:`list` из :obj:`str`): Регион TODO.
        available_as_rbt (:obj:`bool`): TODO.
        content_warning (:obj:`str`): Тип откровенного контента.
        explicit (:obj:`bool`): Содержит ли откровенный контент.
        preview_duration_ms (:obj:`int`): TODO.
        available_full_without_permission (:obj:`bool`): Доступен ли без подписки.
        version (:obj:`str`): Версия.
        remember_position (:obj:`bool`): Если :obj:`True`, то запоминатся последняя позиция прослушивания,
            иначе позиция не запоминается.
        download_info (:obj:`list` из :obj:`yandex_music.DownloadInfo`): Информация о вариантах загрузки трека.
        background_video_uri (:obj:`str`): Ссылка на видеошот.
        short_description (:obj:`str`): Краткое опсание эпизода подкаста.
        is_suitable_for_children (:obj:`bool`): Подходит ли для детей TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`int` | :obj:`str`): Уникальный идентификатор.
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
        type_ (:obj:`str`, optional): Тип.
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
        remember_position (:obj:`bool`, optional): Если :obj:`True`, то запоминатся последняя позиция прослушивания,
            иначе позиция не запоминается.
        background_video_uri (:obj:`str`, optional): Ссылка на видеошот.
        short_description (:obj:`str`, optional): Краткое опсание эпизода подкаста.
        is_suitable_for_children (:obj:`bool`, optional): Подходит ли для детей TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        id_: Union[str, int],
        title: Optional[str] = None,
        available: Optional[bool] = None,
        artists: List['Artist'] = None,
        albums: List['Album'] = None,
        available_for_premium_users: Optional[bool] = None,
        lyrics_available: Optional[bool] = None,
        poetry_lover_matches: List['PoetryLoverMatch'] = None,
        best: Optional[bool] = None,
        real_id: Optional[Union[str, int]] = None,
        og_image: Optional[str] = None,
        type_: Optional[str] = None,
        cover_uri: Optional[str] = None,
        major: Optional['Major'] = None,
        duration_ms: Optional[int] = None,
        storage_dir: Optional[str] = None,
        file_size: Optional[int] = None,
        substituted: Optional['Track'] = None,
        matched_track: Optional['Track'] = None,
        normalization: Optional['Normalization'] = None,
        error: Optional[str] = None,
        can_publish: Optional[bool] = None,
        state: Optional[str] = None,
        desired_visibility: Optional[str] = None,
        filename: Optional[str] = None,
        user_info: Optional['User'] = None,
        meta_data: Optional['MetaData'] = None,
        regions: Optional[List[str]] = None,
        available_as_rbt: Optional[bool] = None,
        content_warning: Optional[str] = None,
        explicit: Optional[bool] = None,
        preview_duration_ms: Optional[int] = None,
        available_full_without_permission: Optional[bool] = None,
        version: Optional[str] = None,
        remember_position: Optional[bool] = None,
        background_video_uri: Optional[str] = None,
        short_description: Optional[str] = None,
        is_suitable_for_children: Optional[bool] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.id = id_

        self.title = title
        self.available = available
        self.artists = artists
        self.albums = albums
        self.available_for_premium_users = available_for_premium_users
        self.lyrics_available = lyrics_available
        self.poetry_lover_matches = poetry_lover_matches
        self.best = best
        self.real_id = real_id
        self.og_image = og_image
        self.type = type_
        self.cover_uri = cover_uri
        self.major = major
        self.duration_ms = duration_ms
        self.storage_dir = storage_dir
        self.file_size = file_size
        self.substituted = substituted
        self.matched_track = matched_track
        self.normalization = normalization
        self.error = error
        self.can_publish = can_publish
        self.state = state
        self.desired_visibility = desired_visibility
        self.filename = filename
        self.user_info = user_info
        self.meta_data = meta_data
        self.regions = regions
        self.available_as_rbt = available_as_rbt
        self.content_warning = content_warning
        self.explicit = explicit
        self.preview_duration_ms = preview_duration_ms
        self.available_full_without_permission = available_full_without_permission
        self.version = version
        self.remember_position = remember_position
        self.background_video_uri = background_video_uri
        self.short_description = short_description
        self.is_suitable_for_children = is_suitable_for_children

        self.download_info = None

        self.client = client
        self._id_attrs = (self.id,)

        super().handle_unknown_kwargs(self, **kwargs)

    def get_download_info(self, get_direct_links=False) -> List['DownloadInfo']:
        """Сокращение для::

        client.tracks_download_info(self.track_id, get_direct_links)
        """
        self.download_info = self.client.tracks_download_info(self.track_id, get_direct_links)

        return self.download_info

    def get_supplement(self, *args, **kwargs) -> Optional['Supplement']:
        """Сокращение для::

        client.track_supplement(track.id, *args, **kwargs)
        """
        return self.client.track_supplement(self.id, *args, **kwargs)

    def download_cover(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.cover_uri.replace("%%", size)}', filename)

    def download_og_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Предпочтительнее использовать `self.download_cover()`.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

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
            :class:`yandex_music.exceptions.InvalidBitrate`: Если в `self.download_info` не найден подходящий трек.
        """
        if self.download_info is None:
            self.get_download_info()

        for info in self.download_info:
            if info.codec == codec and info.bitrate_in_kbps == bitrate_in_kbps:
                info.download(filename)
                break
        else:
            raise InvalidBitrate('Unavailable bitrate')

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_tracks_add(track.id, user.id, *args, **kwargs)
        """
        return self.client.users_likes_tracks_add(self.track_id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

        client.users_likes_tracks_remove(track.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_tracks_remove(self.track_id, self.client.me.account.uid, *args, **kwargs)

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
        from yandex_music import Normalization, Major, Album, Artist, User, MetaData, PoetryLoverMatch

        data['albums'] = Album.de_list(data.get('albums'), client)
        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['normalization'] = Normalization.de_json(data.get('normalization'), client)
        data['major'] = Major.de_json(data.get('major'), client)
        data['substituted'] = Track.de_json(data.get('substituted'), client)
        data['matched_track'] = Track.de_json(data.get('matched_track'), client)
        data['user_info'] = User.de_json(data.get('user_info'), client)
        data['meta_data'] = MetaData.de_json(data.get('meta_data'), client)
        data['poetry_lover_matches'] = PoetryLoverMatch.de_list(data.get('poetry_lover_matches'), client)

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
    #: Псевдоним для :attr:`get_supplement`
    getSupplement = get_supplement
    #: Псевдоним для :attr:`download_cover`
    downloadCover = download_cover
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
    #: Псевдоним для :attr:`track_id`
    trackId = track_id
