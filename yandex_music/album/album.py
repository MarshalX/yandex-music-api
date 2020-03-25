from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Artist, Label, TrackPosition, Track


class Album(YandexMusicObject):
    """Класс, представляющий альбом.

    Note:
        Известные типы альбома: `single` - сингл, `compilation` - сборник.

        Известные предупреждения о содержимом: `explicit` - ненормативная лексика.

        Известные ошибки: `not-found` - альбом с таким ID не существует.

    Attributes:
        id (:obj:`int`): Идентификатор альбома.
        error (:obj:`str`): Ошибка получения альбома.
        title (:obj:`str`): Название альбома.
        track_count (:obj:`int`): Количество треков.
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Артисты.
        labels (:obj:`list` из :obj:`yandex_music.Label`): Лейблы.
        available (:obj:`bool`): Доступен ли альбом.
        available_for_premium_users (:obj:`bool`): Доступен ли альбом для пользователей с подпиской.
        version (:obj:`str`): Дополнительная информация об альбоме.
        cover_uri (:obj:`str`): Ссылка на обложку.
        content_warning (:obj:`str`): Предупреждение о содержимом альбома.
        genre (:obj:`str`): Жанр музыки.
        og_image (:obj:`str`): Ссылка на превью Open Graph.
        recent (:obj:`bool`): Является ли альбом новым.
        very_important (:obj:`bool`): Популярен ли альбом у слушателей.
        available_for_mobile (:obj:`bool`): Доступен ли альбом из приложения для телефона.
        available_partially (:obj:`bool`): Доступен ли альбом частично для пользователей без подписки.
        bests (:obj:`list` из :obj:`int`): ID лучших треков альбома.
        volumes (:obj:`list` из :obj:`list` из :obj:`Track`): Треки альбома, разделенные по дискам.
        year (:obj:`int`): Год релиза.
        release_date (:obj:`str`): Дата релиза в формате ISO 8601.
        type (:obj:`str`): Тип альбома.
        track_position (:obj:`yandex_music.TrackPosition`): Позиция трека в альбоме. Возвращается при получении
            альбома в составе трека.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`int`): Идентификатор альбома.
        error (:obj:`str`, optional): Ошибка получения альбома.
        title (:obj:`str`, optional): Название альбома.
        track_count (:obj:`int`, optional): Количество треков.
        artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Артисты.
        labels (:obj:`list` из :obj:`yandex_music.Label`, optional): Лейблы.
        available (:obj:`bool`, optional): Доступен ли альбом.
        available_for_premium_users (:obj:`bool`, optional): Доступен ли альбом для пользователей с подпиской.
        version (:obj:`str`, optional): Дополнительная информация об альбоме.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        content_warning (:obj:`str`, optional): Предупреждение о содержимом альбома.
        genre (:obj:`str`, optional): Жанр музыки.
        og_image (:obj:`str`, optional): Ссылка на превью Open Graph.
        recent (:obj:`bool`, optional): Является ли альбом новым.
        very_important (:obj:`bool`, optional): Популярен ли альбом у слушателей.
        available_for_mobile (:obj:`bool`, optional): Доступен ли альбом из приложения для телефона.
        available_partially (:obj:`bool`, optional): Доступен ли альбом частично для пользователей без подписки.
        bests (:obj:`list` из :obj:`int`, optional): ID лучших треков альбома.
        volumes (:obj:`list` из :obj:`list` из :obj:`Track`, optional): Треки альбома, разделенные по дискам.
        year (:obj:`int`, optional): Год релиза.
        release_date (:obj:`str`, optional): Дата релиза в формате ISO 8601.
        type_ (:obj:`str`, optional): Тип альбома.
        track_position (:obj:`yandex_music.TrackPosition`, optional): Позиция трека в альбоме. Возвращается при
            получении альбома в составе трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: int,
                 error: Optional[str] = None,
                 title: Optional[str] = None,
                 track_count: Optional[int] = None,
                 artists: List['Artist'] = None,
                 labels: List['Label'] = None,
                 available: Optional[bool] = None,
                 available_for_premium_users: Optional[bool] = None,
                 version: Optional[str] = None,
                 cover_uri: Optional[str] = None,
                 content_warning: Optional[str] = None,
                 original_release_year=None,
                 genre: Optional[str] = None,
                 og_image: Optional[str] = None,
                 buy: Optional[list] = None,
                 recent: Optional[bool] = None,
                 very_important: Optional[bool] = None,
                 available_for_mobile: Optional[bool] = None,
                 available_partially: Optional[bool] = None,
                 bests: Optional[List[int]] = None,
                 prerolls: Optional[list] = None,
                 volumes: Optional[List[List['Track']]] = None,
                 year: Optional[int] = None,
                 release_date: Optional[str] = None,
                 type_: Optional[str] = None,
                 track_position: Optional['TrackPosition'] = None,
                 regions=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.id = id_

        self.error = error
        self.title = title
        self.track_count = track_count
        self.artists = artists
        self.labels = labels
        self.available_for_premium_users = available_for_premium_users
        self.available = available
        self.version = version
        self.cover_uri = cover_uri
        self.genre = genre
        self.year = year
        self.release_date = release_date
        self.bests = bests
        self.prerolls = prerolls
        self.volumes = volumes
        self.og_image = og_image
        self.buy = buy
        self.recent = recent
        self.very_important = very_important
        self.available_for_mobile = available_for_mobile
        self.available_partially = available_partially
        self.type = type_
        self.track_position = track_position
        self.regions = regions
        self.original_release_year = original_release_year
        self.content_warning = content_warning

        self.client = client
        self._id_attrs = (self.id,)

    def with_tracks(self, *args, **kwargs) -> Optional['Album']:
        """Сокращение для::

            client.albums_with_tracks(album.id, *args, **kwargs)
        """
        return self.client.albums_with_tracks(self.id, *args, **kwargs)

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

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_albums_add(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_add(self.id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_albums_remove(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Album']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Album`: Алюбом.
        """
        if not data:
            return None

        data = super(Album, cls).de_json(data, client)
        from yandex_music import Artist, Label, TrackPosition, Track
        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['labels'] = Label.de_list(data.get('labels'), client)
        data['track_position'] = TrackPosition.de_json(data.get('track_position'), client)
        if data.get('volumes'):
            data['volumes'] = [Track.de_list(i, client) for i in data['volumes']]

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Album']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Album`: Альбомы.
        """
        if not data:
            return []

        albums = list()
        for album in data:
            albums.append(cls.de_json(album, client))

        return albums

    # camelCase псевдонимы

    #: Псевдоним для :attr:`with_tracks`
    withTracks = with_tracks
    #: Псевдоним для :attr:`download_cover`
    downloadCover = download_cover
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
