from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        Album,
        AlbumActionButton,
        Artist,
        ArtistLink,
        Chart,
        ClientType,
        Clip,
        Cover,
        CustomWave,
        JSONType,
        Playlist,
        PlaylistId,
        Stats,
        Track,
        UpcomingAlbum,
        Video,
        Vinyl,
    )


@model
class BriefInfo(YandexMusicModel):
    """Класс, представляющий информацию об артисте.

    Attributes:
        artist (:obj:`yandex_music.Artist` | :obj:`None`): Артист.
        albums (:obj:`list` из :obj:`yandex_music.Album`): Альбомы.
        playlists (:obj:`list` из :obj:`yandex_music.Playlist`): Плейлисты.
        also_albums (:obj:`list` из :obj:`yandex_music.Album`): Сборники.
        last_release_ids (:obj:`list` из :obj:`int`): Уникальные идентификаторы последних выпущенных альбомов.
        last_releases (:obj:`list` из :obj:`yandex_music.Album`, optional): Последние выпущенные альбомы.
        popular_tracks (:obj:`list` из :obj:`yandex_music.Track`): Популярные треки.
        similar_artists (:obj:`list` из :obj:`yandex_music.Artist`): Похожие артисты.
        all_covers (:obj:`list` из :obj:`yandex_music.Cover`): Все обложки.
        concerts (:obj:`str`): Концерты (тест-кейс с ними потерялся, мало у кого есть).
        videos (:obj:`list` из :obj:`yandex_music.Video`): Видео.
        vinyls (:obj:`list` из :obj:`yandex_music.Vinyl`): Пластинки.
        has_promotions (:obj:`bool`): Рекламируется ли TODO.
        playlist_ids (:obj:`list` из :obj:`yandex_music.PlaylistId`): Уникальные идентификаторы плейлистов.
        stats (:obj:`yandex_music.Stats`, optional): Статистика прослушиваний за месяц.
        tracks_in_chart (:obj:`list` из :obj:`yandex_music.Chart`, optional): Треки в чарте.
        action_button (:obj:`yandex_music.AlbumActionButton`, optional): Кнопка-действие для перехода по ссылке.
        background_image_url (:obj:`str`, optional): Ссылка на фоновое изображение.
        background_video_id (:obj:`str`, optional): Идентификатор фонового видео.
        background_video_url (:obj:`str`, optional): Ссылка на фоновое видео.
        bandlink_scanner_link (:obj:`yandex_music.ArtistLink`, optional): Ссылка на плейлисты с артистом в Bandlink.
        clips (:obj:`list` из :obj:`yandex_music.Clip`): Клипы. Приходят только с параметром
            `useClipDataFormat=true`.
        custom_wave (:obj:`yandex_music.CustomWave`, optional): Моя волна по артисту.
        has_trailer (:obj:`bool`, optional): Есть ли у артиста трейлер.
        links (:obj:`list` из :obj:`yandex_music.ArtistLink`): Ссылки на страницы артиста.
        upcoming_album (:obj:`yandex_music.UpcomingAlbum`, optional): Предстоящий релиз.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist']
    albums: List['Album']
    playlists: List['Playlist']
    also_albums: List['Album']
    last_release_ids: List[int]
    last_releases: List['Album']
    popular_tracks: List['Track']
    similar_artists: List['Artist']
    all_covers: List['Cover']
    concerts: 'JSONType'
    videos: List['Video']
    vinyls: List['Vinyl']
    has_promotions: bool
    playlist_ids: List['PlaylistId']
    stats: Optional['Stats'] = None
    tracks_in_chart: List['Chart'] = field(default_factory=list)
    action_button: Optional['AlbumActionButton'] = None
    background_image_url: Optional[str] = None
    background_video_id: Optional[str] = None
    background_video_url: Optional[str] = None
    bandlink_scanner_link: Optional['ArtistLink'] = None
    clips: List['Clip'] = field(default_factory=list)
    custom_wave: Optional['CustomWave'] = None
    has_trailer: Optional[bool] = None
    links: List['ArtistLink'] = field(default_factory=list)
    upcoming_album: Optional['UpcomingAlbum'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (
            self.artist,
            self.albums,
            self.playlists,
            self.also_albums,
            self.last_release_ids,
            self.popular_tracks,
            self.similar_artists,
            self.all_covers,
            self.concerts,
            self.videos,
            self.vinyls,
            self.has_promotions,
            self.playlist_ids,
        )
