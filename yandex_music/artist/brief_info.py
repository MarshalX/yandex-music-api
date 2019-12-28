from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Artist, Track, Album, Cover, PlaylistId, Video, Chart, Vinyl

from yandex_music import YandexMusicObject


class BriefInfo(YandexMusicObject):
    def __init__(self,
                 artist: Optional['Artist'],
                 albums: List['Album'],
                 also_albums: List['Album'],
                 last_release_ids: List[int],
                 popular_tracks: List['Track'],
                 similar_artists: List['Artist'],
                 all_covers: List['Cover'],
                 concerts,
                 videos: List['Video'],
                 vinyls: List['Vinyl'],
                 has_promotions: bool,
                 playlist_ids: List['PlaylistId'],
                 tracks_in_chart: List['Chart'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.artist = artist
        self.albums = albums
        self.also_albums = also_albums
        self.last_release_ids = last_release_ids
        self.popular_tracks = popular_tracks
        self.similar_artists = similar_artists
        self.all_covers = all_covers
        self.concerts = concerts
        self.videos = videos
        self.vinyls = vinyls
        self.has_promotions = has_promotions
        self.playlist_ids = playlist_ids

        self.tracks_in_chart = tracks_in_chart

        self.client = client
        self._id_attrs = (self.artist, self.albums, self.also_albums, self.last_release_ids, self.popular_tracks,
                          self.similar_artists, self.all_covers, self.concerts, self.videos, self.vinyls,
                          self.has_promotions, self.playlist_ids)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['BriefInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.BriefInfo`: Объект класса :class:`yandex_music.BriefInfo`.
        """

        if not data:
            return None

        data = super(BriefInfo, cls).de_json(data, client)
        from yandex_music import Artist, Track, Album, Cover, PlaylistId, Video, Chart, Vinyl
        data['artist'] = Artist.de_json(data.get('artist'), client)
        data['similar_artists'] = Artist.de_list(data.get('similar_artists'), client)
        data['popular_tracks'] = Track.de_list(data.get('popular_tracks'), client)
        data['albums'] = Album.de_list(data.get('albums'), client)
        data['also_albums'] = Album.de_list(data.get('also_albums'), client)
        data['all_covers'] = Cover.de_list(data.get('all_covers'), client)
        data['playlist_ids'] = PlaylistId.de_list(data.get('playlist_ids'), client)
        data['videos'] = Video.de_list(data.get('videos'), client)
        data['tracks_in_chart'] = Chart.de_list(data.get('tracks_in_chart'), client)
        data['vinyls'] = Vinyl.de_list(data.get('vinyls'), client)

        return cls(client=client, **data)
