from typing import Dict

import pytest

from yandex_music import (
    Album,
    Artist,
    BriefInfo,
    Chart,
    Client,
    Cover,
    JSONType,
    Playlist,
    PlaylistId,
    Stats,
    Track,
    Video,
    Vinyl,
)


@pytest.fixture(scope='class')
def brief_info(
    artist: Artist,
    track: Track,
    album: Album,
    playlist: Playlist,
    cover: Cover,
    playlist_id: PlaylistId,
    video: Video,
    chart: Chart,
    vinyl: Vinyl,
    stats: Stats,
) -> BriefInfo:
    return BriefInfo(
        artist,
        [album],
        [playlist],
        [album],
        TestBriefInfo.last_release_ids,
        [album],
        [track],
        [artist],
        [cover],
        TestBriefInfo.concerts,
        [video],
        [vinyl],
        TestBriefInfo.has_promotions,
        [playlist_id],
        stats,
        [chart],
    )


class TestBriefInfo:
    last_release_ids = [8501194, 8302547, 8302836, 8302450]
    concerts: JSONType = None
    has_promotions = False

    def test_expected_values(
        self,
        brief_info: BriefInfo,
        artist: Artist,
        track: Track,
        album: Album,
        playlist: Playlist,
        cover: Cover,
        playlist_id: PlaylistId,
        video: Video,
        chart: Chart,
        vinyl: Vinyl,
        stats: Stats,
    ) -> None:
        assert brief_info.artist == artist
        assert brief_info.albums == [album]
        assert brief_info.playlists == [playlist]
        assert brief_info.also_albums == [album]
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.last_releases == [album]
        assert brief_info.popular_tracks == [track]
        assert brief_info.similar_artists == [artist]
        assert brief_info.all_covers == [cover]
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == [video]
        assert brief_info.vinyls == [vinyl]
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == [playlist_id]
        assert brief_info.stats == stats
        assert brief_info.tracks_in_chart == [chart]

    def test_de_json_none(self, client: Client) -> None:
        assert BriefInfo.de_json({}, client) is None

    def test_de_json_required(
        self,
        client: Client,
        artist: Artist,
        track: Track,
        album: Album,
        playlist: Playlist,
        cover: Cover,
        playlist_id: PlaylistId,
        video: Video,
        vinyl: Vinyl,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'albums': [album.to_dict()],
            'also_albums': [album.to_dict()],
            'last_release_ids': self.last_release_ids,
            'last_releases': [album.to_dict()],
            'popular_tracks': [track.to_dict()],
            'similar_artists': [artist.to_dict()],
            'all_covers': [cover.to_dict()],
            'concerts': self.concerts,
            'videos': [video.to_dict()],
            'vinyls': [vinyl.to_dict()],
            'has_promotions': self.has_promotions,
            'playlist_ids': [playlist_id.to_dict()],
            'playlists': [playlist.to_dict()],
        }
        brief_info = BriefInfo.de_json(json_dict, client)
        assert brief_info is not None

        assert brief_info.artist == artist
        assert brief_info.albums == [album]
        assert brief_info.playlists == [playlist]
        assert brief_info.also_albums == [album]
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.last_releases == [album]
        assert brief_info.popular_tracks == [track]
        assert brief_info.similar_artists == [artist]
        assert brief_info.all_covers == [cover]
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == [video]
        assert brief_info.vinyls == [vinyl]
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == [playlist_id]

    def test_de_json_all(
        self,
        client: Client,
        artist: Artist,
        track: Track,
        album: Album,
        playlist: Playlist,
        cover: Cover,
        playlist_id: PlaylistId,
        video: Video,
        chart: Chart,
        vinyl: Vinyl,
        stats: Stats,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'albums': [album.to_dict()],
            'also_albums': [album.to_dict()],
            'last_release_ids': self.last_release_ids,
            'last_releases': [album.to_dict()],
            'popular_tracks': [track.to_dict()],
            'similar_artists': [artist.to_dict()],
            'all_covers': [cover.to_dict()],
            'concerts': self.concerts,
            'videos': [video.to_dict()],
            'vinyls': [vinyl.to_dict()],
            'has_promotions': self.has_promotions,
            'playlist_ids': [playlist_id.to_dict()],
            'tracks_in_chart': [chart.to_dict()],
            'playlists': [playlist.to_dict()],
            'stats': stats.to_dict(),
        }
        brief_info = BriefInfo.de_json(json_dict, client)
        assert brief_info is not None

        assert brief_info.artist == artist
        assert brief_info.albums == [album]
        assert brief_info.playlists == [playlist]
        assert brief_info.also_albums == [album]
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.last_releases == [album]
        assert brief_info.popular_tracks == [track]
        assert brief_info.similar_artists == [artist]
        assert brief_info.all_covers == [cover]
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == [video]
        assert brief_info.vinyls == [vinyl]
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == [playlist_id]
        assert brief_info.stats == stats
        assert brief_info.tracks_in_chart == [chart]

    def test_equality(
        self,
        artist: Artist,
        track: Track,
        album: Album,
        playlist: Playlist,
        cover: Cover,
        playlist_id: PlaylistId,
        video: Video,
        vinyl: Vinyl,
        stats: Stats,
    ) -> None:
        a = BriefInfo(
            artist,
            [album],
            [playlist],
            [album],
            self.last_release_ids,
            [album],
            [track],
            [artist],
            [cover],
            self.concerts,
            [video],
            [vinyl],
            self.has_promotions,
            [playlist_id],
            stats,
        )
        b = BriefInfo(
            artist,
            [album],
            [],
            [album],
            self.last_release_ids,
            [],
            [],
            [artist],
            [cover],
            self.concerts,
            [video],
            [vinyl],
            True,
            [playlist_id],
            stats,
        )
        c = BriefInfo(
            artist,
            [album],
            [playlist],
            [album],
            [1, 2, 3],
            [album],
            [track],
            [artist],
            [],
            self.concerts,
            [video],
            [vinyl],
            self.has_promotions,
            [playlist_id],
            stats,
        )
        d = BriefInfo(
            artist,
            [album],
            [playlist],
            [album],
            self.last_release_ids,
            [album],
            [track],
            [artist],
            [cover],
            self.concerts,
            [video],
            [vinyl],
            self.has_promotions,
            [playlist_id],
            stats,
        )

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
