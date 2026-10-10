from typing import Dict

import pytest

from yandex_music import (
    Album,
    AlbumActionButton,
    Artist,
    ArtistLink,
    BriefInfo,
    Chart,
    Client,
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
    album_action_button: AlbumActionButton,
    artist_link: ArtistLink,
    clip: Clip,
    custom_wave: CustomWave,
    upcoming_album: UpcomingAlbum,
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
        action_button=album_action_button,
        background_image_url=TestBriefInfo.background_image_url,
        background_video_id=TestBriefInfo.background_video_id,
        background_video_url=TestBriefInfo.background_video_url,
        bandlink_scanner_link=artist_link,
        clips=[clip],
        custom_wave=custom_wave,
        has_trailer=TestBriefInfo.has_trailer,
        links=[artist_link],
        upcoming_album=upcoming_album,
    )


class TestBriefInfo:
    last_release_ids = [8501194, 8302547, 8302836, 8302450]
    concerts: JSONType = None
    has_promotions = False
    background_image_url = 'avatars.yandex.net/get-music-misc/12345/artist-background/%%'
    background_video_id = 'fakevideoid100500'
    background_video_url = 'https://example.com/videos/fakevideoid100500.mp4'
    has_trailer = True

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
        album_action_button: AlbumActionButton,
        artist_link: ArtistLink,
        clip: Clip,
        custom_wave: CustomWave,
        upcoming_album: UpcomingAlbum,
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
        assert brief_info.action_button == album_action_button
        assert brief_info.background_image_url == self.background_image_url
        assert brief_info.background_video_id == self.background_video_id
        assert brief_info.background_video_url == self.background_video_url
        assert brief_info.bandlink_scanner_link == artist_link
        assert brief_info.clips == [clip]
        assert brief_info.custom_wave == custom_wave
        assert brief_info.has_trailer == self.has_trailer
        assert brief_info.links == [artist_link]
        assert brief_info.upcoming_album == upcoming_album

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
        album_action_button: AlbumActionButton,
        artist_link: ArtistLink,
        clip: Clip,
        custom_wave: CustomWave,
        upcoming_album: UpcomingAlbum,
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
            'actionButton': album_action_button.to_dict(),
            'backgroundImageUrl': self.background_image_url,
            'backgroundVideoId': self.background_video_id,
            'backgroundVideoUrl': self.background_video_url,
            'bandlinkScannerLink': artist_link.to_dict(),
            'clips': [clip.to_dict()],
            'customWave': custom_wave.to_dict(),
            'hasTrailer': self.has_trailer,
            'links': [artist_link.to_dict()],
            'upcomingAlbum': upcoming_album.to_dict(),
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
        assert brief_info.action_button == album_action_button
        assert brief_info.background_image_url == self.background_image_url
        assert brief_info.background_video_id == self.background_video_id
        assert brief_info.background_video_url == self.background_video_url
        assert brief_info.bandlink_scanner_link == artist_link
        assert brief_info.clips == [clip]
        assert brief_info.custom_wave == custom_wave
        assert brief_info.has_trailer == self.has_trailer
        assert brief_info.links == [artist_link]
        assert brief_info.upcoming_album == upcoming_album

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
