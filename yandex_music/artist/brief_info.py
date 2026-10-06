from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        Album,
        Artist,
        Chart,
        ClientType,
        Cover,
        JSONType,
        Playlist,
        PlaylistId,
        Stats,
        Track,
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
