from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, User, Cover, MadeFor, TrackShort, PlaylistAbsence, PlayCounter


class Playlist(YandexMusicObject):
    """Класс, представляющий плейлист.

    Note:
        Известные значения `visibility`: `public` - публичный плейлист, `private` - приватный плейлист.

        Известные значения `generated_playlist_type`: `playlistOfTheDay` - Плейлист дня, `recentTracks` - Премьера,
        `neverHeard` - Дежавю, `podcasts` - Подкасты недели, `missedLikes` - Тайник, `origin` - Плейлист с Алисой.

    Attributes:
        owner (:obj:`yandex_music.User`): Владелец плейлиста.
        cover (:obj:`yandex_music.Cover`): Обложка альбома.
        made_for (:obj:`yandex_music.MadeFor`): Пользователь для которого был создан плейлист. Присутствует только у
            персональных плейлистов.
        play_counter (:obj:`yandex_music.PlayCounter`): Счетчик дней. Присутствует только у плейлиста дня.
        playlist_absence (:obj:`yandex_music.PlaylistAbsence`): Причина отсутствия плейлиста.
        uid (:obj:`int`): Идентификатор владельца плейлиста.
        kind (:obj:`int`): Идентификатор плейлиста.
        title (:obj:`str`): Название плейлиста.
        track_count (:obj:`int`): Количество треков.
        tags (:obj:`list`): Список тегов плейлиста.
        revision (:obj:`int`): Актуальность данных TODO.
        snapshot (:obj:`int`): Версия плейлиста. Увеличивается на 1 при каждом изменении.
        visibility (:obj:`str`): Видимость плейлиста.
        collective (:obj:`bool`): Есть ли у плейлиста соавторы.
        created (:obj:`str`): Дата создания в формате ISO 8601.
        modified (:obj:`str`): Дата последнего изменения в формате ISO 8601.
        available (:obj:`bool`): Доступен TODO.
        is_banner (:obj:`bool`): Является ли банером TODO.
        is_premiere (:obj:`bool`): Является ли премьерой TODO.
        duration_ms (:obj:`int`): Длительность в миллисекундах.
        og_image (:obj:`str`): Ссылка на превью Open Graph.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`): Список треков.
        prerolls (:obj:`list`): Прерол, проигрываемый перед плейлистом. Присутствует только у персональных плейлистов.
        likes_count (:obj:`int`): Количество лайков.
        generated_playlist_type (:obj:`str`): Тип генерируемого плейлиста.
        animated_cover_uri (:obj:`str`): Ссылка на анимированную обложку.
        ever_played (:obj:`str`): Играл ли этот плейлист. Присутствует только у персональных плейлистов. TODO
        description (:obj:`str`): Описание плейлиста с разметкой Markdown.
        description_formatted (:obj:`str`): Описание плейлиста. Только текст, без разметки.
        is_for_from: TODO.
        regions: Регион TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        owner (:obj:`yandex_music.User`, optional): Владелец плейлиста.
        cover (:obj:`yandex_music.Cover`, optional): Обложка альбома.
        made_for (:obj:`yandex_music.MadeFor`, optional): Пользователь для которого был создан плейлист. Присутствует только у
            персональных плейлистов.
        play_counter (:obj:`yandex_music.PlayCounter`, optional): Счетчик дней. Присутствует только у плейлиста дня.
        playlist_absence (:obj:`yandex_music.PlaylistAbsence`, optional): Причина отсутствия плейлиста.
        uid (:obj:`int`, optional): Идентификатор владельца плейлиста.
        kind (:obj:`int`, optional): Идентификатор плейлиста.
        title (:obj:`str`, optional): Название плейлиста.
        track_count (:obj:`int`, optional): Количество треков.
        tags (:obj:`list`, optional): Список тегов плейлиста.
        revision (:obj:`int`, optional): Актуальность данных TODO.
        snapshot (:obj:`int`, optional): Версия плейлиста. Увеличивается на 1 при каждом изменении.
        visibility (:obj:`str`, optional): Видимость плейлиста.
        collective (:obj:`bool`, optional): Есть ли у плейлиста соавторы.
        created (:obj:`str`, optional): Дата создания в формате ISO 8601.
        modified (:obj:`str`, optional): Дата последнего изменения в формате ISO 8601.
        available (:obj:`bool`, optional): Доступен TODO.
        is_banner (:obj:`bool`, optional): Является ли банером TODO.
        is_premiere (:obj:`bool`, optional): Является ли премьерой TODO.
        duration_ms (:obj:`int`, optional): Длительность в миллисекундах.
        og_image (:obj:`str`, optional): Ссылка на превью Open Graph.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`, optional): Список треков.
        prerolls (:obj:`list`, optional): Прерол, проигрываемый перед плейлистом. Присутствует только у персональных
            плейлистов.
        likes_count (:obj:`int`, optional): Количество лайков.
        generated_playlist_type (:obj:`str`, optional): Тип генерируемого плейлиста.
        animated_cover_uri (:obj:`str`, optional): Ссылка на анимированную обложку.
        ever_played (:obj:`str`, optional): Играл ли этот плейлист. Присутствует только у персональных плейлистов. TODO
        description (:obj:`str`, optional): Описание плейлиста с разметкой Markdown.
        description_formatted (:obj:`str`, optional): Описание плейлиста. Только текст, без разметки.
        is_for_from: TODO.
        regions: Регион TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 owner: Optional['User'],
                 cover: Optional['Cover'],
                 made_for: Optional['MadeFor'],
                 play_counter: Optional['PlayCounter'],
                 playlist_absence: Optional['PlaylistAbsence'],
                 uid: Optional[int] = None,
                 kind: Optional[int] = None,
                 title: Optional[str] = None,
                 track_count: Optional[int] = None,
                 tags: Optional[list] = None,
                 revision: Optional[int] = None,
                 snapshot: Optional[int] = None,
                 visibility: Optional[str] = None,
                 collective: Optional[bool] = None,
                 created: Optional[str] = None,
                 modified: Optional[str] = None,
                 available: Optional[bool] = None,
                 is_banner: Optional[bool] = None,
                 is_premiere: Optional[bool] = None,
                 duration_ms: Optional[int] = None,
                 og_image: Optional[str] = None,
                 tracks: List['TrackShort'] = None,
                 prerolls: Optional[list] = None,
                 likes_count: Optional[int] = None,
                 generated_playlist_type: Optional[str] = None,
                 animated_cover_uri: Optional[str] = None,
                 ever_played: Optional[bool] = None,
                 description: Optional[str] = None,
                 description_formatted: Optional[str] = None,
                 is_for_from=None,
                 regions=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.owner = owner
        self.cover = cover
        self.made_for = made_for
        self.play_counter = play_counter
        self.playlist_absence = playlist_absence

        self.uid = uid
        self.kind = kind
        self.title = title
        self.track_count = track_count
        self.revision = revision
        self.snapshot = snapshot
        self.visibility = visibility
        self.collective = collective
        self.created = created
        self.modified = modified
        self.available = available
        self.is_banner = is_banner
        self.is_premiere = is_premiere
        self.duration_ms = duration_ms
        self.og_image = og_image
        self.tracks = tracks
        self.prerolls = prerolls
        self.likes_count = likes_count
        self.animated_cover_uri = animated_cover_uri
        self.description = description
        self.description_formatted = description_formatted
        self.ever_played = ever_played
        self.generated_playlist_type = generated_playlist_type
        self.is_for_from = is_for_from
        self.regions = regions
        self.tags = tags

        self.client = client
        self._id_attrs = (self.uid, self.kind, self.title, self.playlist_absence)

    @property
    def is_mine(self) -> bool:
        return self.owner.uid == self.client.me.account.uid

    @property
    def playlist_id(self) -> str:
        return f'{self.owner.uid}:{self.kind}'

    def download_animated_cover(self, filename: str, size: str = '200x200') -> None:
        """Загрузка анимированной обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением (GIF).
            size (:obj:`str`, optional): Размер анимированной обложки.
        """
        self.client.request.download(f'https://{self.animated_cover_uri.replace("%%", size)}', filename)

    def download_og_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

    def rename(self, name: str) -> None:
        client, kind = self.client, self.kind

        self.__dict__.clear()
        self.__dict__.update(client.users_playlists_name(kind, name).__dict__)

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_playlists_add(playlist.uid, user.id *args, **kwargs)
        """
        return self.client.users_likes_playlists_add(self.uid, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_playlists_remove(playlist.uid, user.id *args, **kwargs)
        """
        return self.client.users_likes_playlists_remove(self.uid, self.client.me.account.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Playlist']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Playlist`: Плейлист.
        """
        if not data:
            return None

        data = super(Playlist, cls).de_json(data, client)
        from yandex_music import User, MadeFor, Cover, PlayCounter, TrackShort, PlaylistAbsence
        data['owner'] = User.de_json(data.get('owner'), client)
        data['cover'] = Cover.de_json(data.get('cover'), client)
        data['made_for'] = MadeFor.de_json(data.get('made_for'), client)
        data['tracks'] = TrackShort.de_list(data.get('tracks'), client)
        data['play_counter'] = PlayCounter.de_json(data.get('play_counter'), client)

        data['playlist_absence'] = PlaylistAbsence.de_json(data.get('playlist_absence'), client)    # на случай фикса
        if data.get('playlist_absense'):    # очепятка яндуха
            data['playlist_absence'] = PlaylistAbsence.de_json(data.get('playlist_absense'), client)
            data.pop('playlist_absense')

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Playlist']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist`: Плейлисты.
        """
        if not data:
            return []

        playlists = list()
        for playlist in data:
            playlists.append(cls.de_json(playlist, client))

        return playlists

    # camelCase псевдонимы

    #: Псевдоним для :attr:`is_mine`
    isMine = is_mine
    #: Псевдоним для :attr:`playlist_id`
    playlistId = playlist_id
    #: Псевдоним для :attr:`download_animated_cover`
    downloadAnimatedCover = download_animated_cover
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
