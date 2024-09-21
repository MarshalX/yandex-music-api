from dataclasses import field
from typing import TYPE_CHECKING, Any, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        Artist,
        Brand,
        ClientType,
        Contest,
        Cover,
        CustomWave,
        JSONType,
        MadeFor,
        OpenGraphData,
        Pager,
        PlayCounter,
        PlaylistAbsence,
        PlaylistRecommendations,
        TrackId,
        TrackShort,
        User,
    )


@model
class Playlist(YandexMusicModel):
    """Класс, представляющий плейлист.

    Note:
        Под полями с заглушками понимаются поля, которые доступны у умных плейлистов тогда, когда у сервиса мало
        данных для генерации плейлиста.

        Известные значения `visibility`: `public` - публичный плейлист, `private` - приватный плейлист.

        Известные значения `generated_playlist_type`: `playlistOfTheDay` - Плейлист дня, `recentTracks` - Премьера,
        `neverHeard` - Дежавю, `podcasts` - Подкасты недели, `missedLikes` - Тайник, `origin` - Плейлист с Алисой.

        Известные значения `type`: `missedLikes`, `recentTracks`.

    Attributes:
        owner (:obj:`yandex_music.User`, optional): Владелец плейлиста.
        cover (:obj:`yandex_music.Cover`, optional): Обложка альбома.
        made_for (:obj:`yandex_music.MadeFor`, optional): Пользователь для которого был создан плейлист. Присутствует
            только у персональных плейлистов.
        play_counter (:obj:`yandex_music.PlayCounter`, optional): Счётчик дней. Присутствует только у плейлиста дня.
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
        url_part (:obj:`str`, optional): Часть ссылки на плейлист ('daily`).
        created (:obj:`str`, optional): Дата создания в формате ISO 8601.
        modified (:obj:`str`, optional): Дата последнего изменения в формате ISO 8601.
        available (:obj:`bool`, optional): Доступен TODO.
        is_banner (:obj:`bool`, optional): Является ли банером TODO.
        is_premiere (:obj:`bool`, optional): Является ли премьерой TODO.
        duration_ms (:obj:`int`, optional): Длительность в миллисекундах.
        og_image (:obj:`str`, optional): Ссылка на превью Open Graph.
        og_title (:obj:`str`, optional): Заголовок Open Graph.
        og_description (:obj:`str`, optional): Описание Open Graph.
        image (:obj:`str`, optional): Изображение TODO.
        cover_without_text (:obj:`yandex_music.Cover`, optional): Обложка без текста.
        contest (:obj:`yandex_music.Contest`, optional): Контест TODO.
        background_color (:obj:`str`, optional): Цвет заднего фона TODO.
        text_color (:obj:`str`, optional): Цвет текста TODO.
        id_for_from (:obj:`str`, optional): Откуда пришло событие (уникальный идентификатор объекта) TODO.
        dummy_description (:obj:`str`, optional): Описание-заглушка плейлиста.
        dummy_page_description (:obj:`str`, optional): Описание-заглушка страницы.
        dummy_cover (:obj:`str`, optional): Обложка-заглушка.
        dummy_rollover_cover (:obj:`str`, optional): Обложка-заглушка TODO.
        og_data (:obj:`yandex_music.OpenGraphData`, optional): Данные для OpenGraph.
        branding (:obj:`yandex_music.Brand`): Бренд.
        metrika_id (:obj:`int`, optional): Уникальный идентификатор счётчика на Яндекс.Метрика.
        coauthors (:obj:`list` из :obj:`int`, optional): Перечень ID аккаунтов соавторов плейлиста.
        top_artist (:obj:`list` из :obj:`yandex_music.Artist`, optional): Топ артистов TODO.
        recent_tracks (:obj:`list` из :obj:`yandex_music.TrackId`, optional): Список ID недавних треков.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`, optional): Список треков.
        prerolls (:obj:`list`, optional): Прерол, проигрываемый перед плейлистом. Присутствует только у персональных
            плейлистов.
        likes_count (:obj:`int`, optional): Количество лайков.
        similar_playlists (:obj:`list` из :obj:`yandex_music.Playlist`, optional): Похожие плейлисты.
        last_owner_playlists (:obj:`list` из :obj:`yandex_music.Playlist`, optional): Последние плейлисты владельца.
        generated_playlist_type (:obj:`str`, optional): Тип генерируемого плейлиста.
        animated_cover_uri (:obj:`str`, optional): Ссылка на анимированную обложку.
        ever_played (:obj:`str`, optional): Играл ли этот плейлист. Присутствует только у персональных плейлистов. TODO
        description (:obj:`str`, optional): Описание плейлиста с разметкой Markdown.
        description_formatted (:obj:`str`, optional): Описание плейлиста. Только текст, без разметки.
        playlist_uuid (:obj:`str`, optional): TODO.
        type (:obj:`str`, optional): TODO.
        ready (:obj:`bool`, optional): Готовность TODO.
        is_for_from: TODO.
        regions: Регион TODO.
        custom_wave (:obj:'yandex_music.CustomWave`, optional): Описание плейлиста. TODO.
        pager (:obj:`yandex_music.Pager`, optional): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    owner: Optional['User']
    cover: Optional['Cover']
    made_for: Optional['MadeFor']
    play_counter: Optional['PlayCounter']
    playlist_absence: Optional['PlaylistAbsence']
    uid: Optional[int] = None
    kind: Optional[int] = None
    title: Optional[str] = None
    track_count: Optional[int] = None
    tags: Optional[list] = None
    revision: Optional[int] = None
    snapshot: Optional[int] = None
    visibility: Optional[str] = None
    collective: Optional[bool] = None
    url_part: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    available: Optional[bool] = None
    is_banner: Optional[bool] = None
    is_premiere: Optional[bool] = None
    duration_ms: Optional[int] = None
    og_image: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    image: Optional[str] = None
    cover_without_text: Optional['Cover'] = None
    contest: Optional['Contest'] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    id_for_from: Optional[str] = None
    dummy_description: Optional[str] = None
    dummy_page_description: Optional[str] = None
    dummy_cover: Optional['Cover'] = None
    dummy_rollover_cover: Optional['Cover'] = None
    og_data: Optional['OpenGraphData'] = None
    branding: Optional['Brand'] = None
    metrika_id: Optional[int] = None
    coauthors: List[int] = field(default_factory=list)
    top_artist: List['Artist'] = field(default_factory=list)
    recent_tracks: List['TrackId'] = field(default_factory=list)
    tracks: List['TrackShort'] = field(default_factory=list)
    prerolls: Optional[list] = None
    likes_count: Optional[int] = None
    similar_playlists: List['Playlist'] = field(default_factory=list)
    last_owner_playlists: List['Playlist'] = field(default_factory=list)
    generated_playlist_type: Optional[str] = None
    animated_cover_uri: Optional[str] = None
    ever_played: Optional[bool] = None
    description: Optional[str] = None
    description_formatted: Optional[str] = None
    playlist_uuid: Optional[str] = None
    type: Optional[str] = None
    ready: Optional[bool] = None
    is_for_from: Any = None
    regions: Any = None
    custom_wave: Optional['CustomWave'] = None
    pager: Optional['Pager'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.uid, self.kind, self.title, self.playlist_absence)

    @property
    def is_mine(self) -> bool:
        """Является ли плейлист моим."""
        if not self.owner or not self.client:
            return False
        return str(self.owner.uid) == self.client.account_uid

    @property
    def playlist_id(self) -> str:
        """Полный ID плейлиста."""
        if self.owner:
            return f'{self.owner.uid}:{self.kind}'
        return str(self.kind)

    def get_recommendations(self, *args: Any, **kwargs: Any) -> Optional['PlaylistRecommendations']:
        """Сокращение для::

        client.users_playlists_recommendations(playlist.kind, playlist.owner.uid, *args, **kwargs)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert self.valid_client(self.client)
        return self.client.users_playlists_recommendations(self.kind, self.owner.uid, *args, **kwargs)

    async def get_recommendations_async(self, *args: Any, **kwargs: Any) -> Optional['PlaylistRecommendations']:
        """Сокращение для::

        await client.users_playlists_recommendations(playlist.kind, playlist.owner.uid, *args, **kwargs)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert self.valid_async_client(self.client)
        return await self.client.users_playlists_recommendations(self.kind, self.owner.uid, *args, **kwargs)

    def get_animated_cover_url(self, size: str = '300x300') -> str:
        """Возвращает URL анимированной обложки.

        Args:
            size (:obj:`str`, optional): Размер анимированной обложки.

        Returns:
            :obj:`str`: URL анимированной обложки.
        """
        assert isinstance(self.animated_cover_uri, str)
        return f'https://{self.animated_cover_uri.replace("%%", size)}'

    def get_og_image_url(self, size: str = '300x300') -> str:
        """Возвращает URL обложки.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`str`: URL обложки.
        """
        assert isinstance(self.og_image, str)
        return f'https://{self.og_image.replace("%%", size)}'

    def download_animated_cover(self, filename: str, size: str = '200x200') -> None:
        """Загрузка анимированной обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением (GIF).
            size (:obj:`str`, optional): Размер анимированной обложки.
        """
        assert self.valid_client(self.client)
        self.client.request.download(self.get_animated_cover_url(size), filename)

    async def download_animated_cover_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка анимированной обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением (GIF).
            size (:obj:`str`, optional): Размер анимированной обложки.
        """
        assert self.valid_async_client(self.client)
        await self.client.request.download(self.get_animated_cover_url(size), filename)

    def download_og_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        assert self.valid_client(self.client)
        self.client.request.download(self.get_og_image_url(size), filename)

    async def download_og_image_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        assert self.valid_async_client(self.client)
        await self.client.request.download(self.get_og_image_url(size), filename)

    def download_animated_cover_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка анимированной обложки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер анимированной обложки.

        Returns:
            :obj:`bytes`: Анимированная обложка в виде байтов.
        """
        assert self.valid_client(self.client)
        return self.client.request.retrieve(self.get_animated_cover_url(size))

    async def download_animated_cover_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка анимированной обложки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер анимированной обложки.

        Returns:
            :obj:`bytes`: Анимированная обложка в виде байтов.
        """
        assert self.valid_async_client(self.client)
        return await self.client.request.retrieve(self.get_animated_cover_url(size))

    def download_og_image_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Используйте это только когда нет self.cover!

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        assert self.valid_client(self.client)
        return self.client.request.retrieve(self.get_og_image_url(size))

    async def download_og_image_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Используйте это только когда нет self.cover!

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        assert self.valid_async_client(self.client)
        return await self.client.request.retrieve(self.get_og_image_url(size))

    def rename(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Сокращение для::

        client.users_playlists_name(playlist.kind, name, *args, **kwargs)
        """
        assert self.valid_client(self.client)
        assert isinstance(self.kind, int)
        client, kind = self.client, self.kind

        self.__dict__.clear()
        self.__dict__.update(client.users_playlists_name(kind, name, *args, **kwargs).__dict__)

    async def rename_async(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Сокращение для::

        client.users_playlists_name(playlist.kind, name, *args, **kwargs)
        """
        assert self.valid_async_client(self.client)
        assert isinstance(self.kind, int)
        client, kind = self.client, self.kind

        self.__dict__.clear()
        self.__dict__.update((await client.users_playlists_name(kind, name, *args, **kwargs)).__dict__)

    def like(self, *args: Any, **kwargs: Any) -> bool:
        """Сокращение для::

        client.users_likes_playlists_add(playlist.playlist_id, user.id, *args, **kwargs)
        """
        assert self.valid_client(self.client)
        return self.client.users_likes_playlists_add(self.playlist_id, self.client.account_uid, *args, **kwargs)

    async def like_async(self, *args: Any, **kwargs: Any) -> bool:
        """Сокращение для::

        await client.users_likes_playlists_add(playlist.playlist_id, user.id, *args, **kwargs)
        """
        assert self.valid_async_client(self.client)
        return await self.client.users_likes_playlists_add(self.playlist_id, self.client.account_uid, *args, **kwargs)

    def dislike(self, *args: Any, **kwargs: Any) -> bool:
        """Сокращение для::

        client.users_likes_playlists_remove(playlist.playlist_id, user.id, *args, **kwargs)
        """
        assert self.valid_client(self.client)
        return self.client.users_likes_playlists_remove(self.playlist_id, self.client.account_uid, *args, **kwargs)

    async def dislike_async(self, *args: Any, **kwargs: Any) -> bool:
        """Сокращение для::

        await client.users_likes_playlists_remove(playlist.playlist_id, user.id, *args, **kwargs)
        """
        assert self.valid_async_client(self.client)
        return await self.client.users_likes_playlists_remove(
            self.playlist_id, self.client.account_uid, *args, **kwargs
        )

    def fetch_tracks(self, *args: Any, **kwargs: Any) -> List['TrackShort']:
        """Сокращение для::

        client.users_playlists(playlist.kind, playlist.owner.id, *args, **kwargs).tracks
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert self.valid_client(self.client)

        playlist = self.client.users_playlists(self.kind, self.owner.uid, *args, **kwargs)
        assert isinstance(playlist, Playlist)
        return playlist.tracks

    async def fetch_tracks_async(self, *args: Any, **kwargs: Any) -> List['TrackShort']:
        """Сокращение для::

        await client.users_playlists(playlist.kind, playlist.owner.id, *args, **kwargs).tracks
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert self.valid_async_client(self.client)

        playlist = await self.client.users_playlists(self.kind, self.owner.uid, *args, **kwargs)
        assert isinstance(playlist, Playlist)
        return playlist.tracks

    def insert_track(self, track_id: int, album_id: int, **kwargs: Any) -> Optional['Playlist']:
        """Сокращение для::

        client.users_playlists_insert_track(self.kind, track_id, album_id, user_id=self.owner.uid,
        revision=self.revision, *args, **kwargs)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert isinstance(self.revision, int)
        assert self.valid_client(self.client)
        return self.client.users_playlists_insert_track(
            self.kind, track_id, album_id, user_id=self.owner.uid, revision=self.revision, **kwargs
        )

    async def insert_track_async(self, track_id: int, album_id: int, **kwargs: Any) -> Optional['Playlist']:
        """Сокращение для::

        await client.users_playlists_insert_track(self.kind, track_id, album_id, user_id=self.owner.uid,
        revision=self.revision, *args, **kwargs)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert isinstance(self.revision, int)
        assert self.valid_async_client(self.client)
        return await self.client.users_playlists_insert_track(
            self.kind, track_id, album_id, user_id=self.owner.uid, revision=self.revision, **kwargs
        )

    def delete_tracks(self, from_: int, to: int, *args: Any, **kwargs: Any) -> Optional['Playlist']:
        """Сокращение для::

        client.users_playlists_delete_track(self.kind, from_, to, self.revision, self.owner.uid, *args, **kwargs)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert isinstance(self.revision, int)
        assert self.valid_client(self.client)
        return self.client.users_playlists_delete_track(
            self.kind, from_, to, self.revision, self.owner.uid, *args, **kwargs
        )

    async def delete_tracks_async(self, from_: int, to: int, *args: Any, **kwargs: Any) -> Optional['Playlist']:
        """Сокращение для::

        await client.users_playlists_delete_track(self.kind, from_, to, self.revision, self.owner.uid, *args, **kwargs)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert isinstance(self.revision, int)
        assert self.valid_async_client(self.client)
        return await self.client.users_playlists_delete_track(
            self.kind, from_, to, self.revision, self.owner.uid, *args, **kwargs
        )

    def delete(self, *args: Any, **kwargs: Any) -> bool:
        """Сокращение для::

        client.users_playlists_delete(self.kind, self.owner.uid)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert self.valid_client(self.client)
        return self.client.users_playlists_delete(self.kind, self.owner.uid, *args, **kwargs)

    async def delete_async(self, *args: Any, **kwargs: Any) -> bool:
        """Сокращение для::

        await client.users_playlists_delete(self.kind, self.owner.uid)
        """
        assert self.owner
        assert isinstance(self.kind, int)
        assert self.valid_async_client(self.client)
        return await self.client.users_playlists_delete(self.kind, self.owner.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Playlist']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Playlist`: Плейлист.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import (
            Artist,
            Brand,
            Contest,
            Cover,
            CustomWave,
            MadeFor,
            OpenGraphData,
            Pager,
            PlayCounter,
            PlaylistAbsence,
            TrackId,
            TrackShort,
            User,
        )

        cls_data['owner'] = User.de_json(data.get('owner'), client)
        cls_data['cover'] = Cover.de_json(data.get('cover'), client)
        cls_data['cover_without_text'] = Cover.de_json(data.get('cover_without_text'), client)
        cls_data['made_for'] = MadeFor.de_json(data.get('made_for'), client)
        cls_data['tracks'] = TrackShort.de_list(data.get('tracks'), client)
        cls_data['recent_tracks'] = TrackId.de_list(data.get('recent_tracks'), client)
        cls_data['play_counter'] = PlayCounter.de_json(data.get('play_counter'), client)
        cls_data['top_artist'] = Artist.de_list(data.get('top_artist'), client)
        cls_data['contest'] = Contest.de_json(data.get('contest'), client)
        cls_data['og_data'] = OpenGraphData.de_json(data.get('og_data'), client)
        cls_data['dummy_cover'] = Cover.de_json(data.get('dummy_cover'), client)
        cls_data['dummy_rollover_cover'] = Cover.de_json(data.get('dummy_rollover_cover'), client)
        cls_data['branding'] = Brand.de_json(data.get('branding'), client)

        cls_data['similar_playlists'] = Playlist.de_list(data.get('similar_playlists'), client)
        cls_data['last_owner_playlists'] = Playlist.de_list(data.get('last_owner_playlists'), client)

        cls_data['playlist_absence'] = PlaylistAbsence.de_json(data.get('playlist_absence'), client)  # на случай фикса
        if data.get('playlist_absense'):  # очепятка яндуха
            cls_data['playlist_absence'] = PlaylistAbsence.de_json(data.get('playlist_absense'), client)
            cls_data.pop('playlist_absense')

        cls_data['custom_wave'] = CustomWave.de_json(data.get('custom_wave'), client)
        cls_data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`is_mine`
    isMine = is_mine
    #: Псевдоним для :attr:`playlist_id`
    playlistId = playlist_id
    #: Псевдоним для :attr:`get_recommendations`
    getRecommendations = get_recommendations
    #: Псевдоним для :attr:`get_recommendations_async`
    getRecommendationsAsync = get_recommendations_async
    #: Псевдоним для :attr:`get_animated_cover_url`
    getAnimatedCoverUrl = get_animated_cover_url
    #: Псевдоним для :attr:`get_og_image_url`
    getOgImageUrl = get_og_image_url
    #: Псевдоним для :attr:`download_animated_cover`
    downloadAnimatedCover = download_animated_cover
    #: Псевдоним для :attr:`download_animated_cover_async`
    downloadAnimatedCoverAsync = download_animated_cover_async
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
    #: Псевдоним для :attr:`download_og_image_async`
    downloadOgImageAsync = download_og_image_async
    #: Псевдоним для :attr:`download_animated_cover_bytes`
    downloadAnimatedCoverBytes = download_animated_cover_bytes
    #: Псевдоним для :attr:`download_animated_cover_bytes_async`
    downloadAnimatedCoverBytesAsync = download_animated_cover_bytes_async
    #: Псевдоним для :attr:`download_og_image_bytes`
    downloadOgImageBytes = download_og_image_bytes
    #: Псевдоним для :attr:`download_og_image_bytes_async`
    downloadOgImageBytesAsync = download_og_image_bytes_async
    #: Псевдоним для :attr:`rename_async`
    renameAsync = rename_async
    #: Псевдоним для :attr:`like_async`
    likeAsync = like_async
    #: Псевдоним для :attr:`dislike_async`
    dislikeAsync = dislike_async
    #: Псевдоним для :attr:`fetch_tracks`
    fetchTracks = fetch_tracks
    #: Псевдоним для :attr:`fetch_tracks_async`
    fetchTracksAsync = fetch_tracks_async
    #: Псевдоним для :attr:`insert_track`
    insertTrack = insert_track
    #: Псевдоним для :attr:`insert_track_async`
    insertTrackAsync = insert_track_async
    #: Псевдоним для :attr:`delete_tracks`
    deleteTracks = delete_tracks
    #: Псевдоним для :attr:`delete_tracks_async`
    deleteTracksAsync = delete_tracks_async
    #: Псевдоним для :attr:`delete_async`
    deleteAsync = delete_async
