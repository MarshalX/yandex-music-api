from typing import Dict, List, Optional, Tuple, Union

import pytest

from yandex_music import (
    R128,
    Account,
    AdParams,
    Album,
    AlbumActionButton,
    AlbumEvent,
    AlbumSimilarEntities,
    AlbumTrailer,
    Alert,
    AlertButton,
    Artist,
    ArtistAbout,
    ArtistClipData,
    ArtistClipItem,
    ArtistClips,
    ArtistConcerts,
    ArtistDonationData,
    ArtistDonationGoal,
    ArtistDonationItem,
    ArtistDonations,
    ArtistEvent,
    ArtistInfo,
    ArtistLink,
    ArtistLinks,
    ArtistSimilar,
    ArtistSkeleton,
    ArtistTrailer,
    ArtistTrailerStatus,
    AutoRenewable,
    Best,
    Block,
    BlockEntity,
    Brand,
    CaseForms,
    Chart,
    ChartInfo,
    ChartInfoMenu,
    ChartInfoMenuItem,
    ChartItem,
    Client,
    Clip,
    ClipsWillLike,
    CombinedSession,
    CombinedSessionItem,
    CombinedSessionLanding,
    CombinedSessionQueueItem,
    Concert,
    ConcertCashback,
    ConcertDescription,
    ConcertEventInfo,
    ConcertFeed,
    ConcertFeedItem,
    ConcertFeedItemData,
    ConcertInfo,
    ConcertLocation,
    ConcertLocations,
    ConcertMinPrice,
    ConcertSkeleton,
    ConcertTabConfig,
    ConcertTabConfigData,
    ConcertTabRange,
    ContentRestrictions,
    Contest,
    Context,
    Counts,
    Cover,
    CoverDerivedColors,
    Credit,
    Credits,
    CustomWave,
    Day,
    Deactivation,
    Deprecation,
    Description,
    DeviceCode,
    Disclaimer,
    DiscreteScale,
    Enum,
    Event,
    ExperimentDetail,
    ExperimentDetailValue,
    ExperimentsDetails,
    Fade,
    FileDownloadInfo,
    FileInfo,
    ForeignAgent,
    GeneratedPlaylist,
    GenerativeStream,
    GenerativeStreamData,
    GenerativeStreamFeedback,
    GenerativeStreamInfo,
    Icon,
    Id,
    Images,
    InvocationInfo,
    Label,
    LicenceTextPart,
    Link,
    Lyrics,
    LyricsInfo,
    LyricsMajor,
    MadeFor,
    Major,
    MetaData,
    Metatag,
    MetatagAlbums,
    MetatagArtistEntry,
    MetatagArtists,
    MetatagLeaf,
    MetatagPlaylists,
    Metatags,
    MetatagSortByValue,
    MetatagTitle,
    MetatagTree,
    MixLink,
    MusicHistory,
    MusicHistoryContextFullModel,
    MusicHistoryGroup,
    MusicHistoryItem,
    MusicHistoryItemData,
    MusicHistoryItemId,
    MusicHistoryItems,
    MusicHistoryTab,
    NonAutoRenewable,
    Normalization,
    OAuthToken,
    OpenGraphData,
    Operator,
    Pager,
    PassportPhone,
    Permissions,
    PersonalPlaylistsData,
    Pin,
    PinData,
    PinsList,
    PlayContext,
    PlayContextsData,
    PlayCounter,
    Playlist,
    PlaylistAbsence,
    PlaylistAvailability,
    PlaylistId,
    PlaylistSimilarEntities,
    PlaylistsList,
    PlaylistTrailer,
    Plus,
    PoetryLoverMatch,
    Presaves,
    Price,
    Product,
    Promotion,
    Ratings,
    RenewableRemainder,
    Restrictions,
    RotorSeed,
    RotorSession,
    RotorSessionTracks,
    RotorSettings,
    SearchResult,
    Sequence,
    SessionEvent,
    SessionFeedback,
    SessionFeedbacks,
    SessionPlayable,
    Settings,
    Shot,
    ShotData,
    ShotType,
    SimilarEntityData,
    SimilarEntityItem,
    SkeletonBlock,
    SkeletonBlockData,
    SkeletonSource,
    SkeletonTab,
    SkeletonViewAllAction,
    SmartPreviewParams,
    Station,
    StationData,
    StationResult,
    Stats,
    Status,
    Subscription,
    Tag,
    Title,
    Track,
    TrackFullInfo,
    TrackId,
    TrackLyrics,
    TrackParameters,
    TrackPosition,
    TrackShort,
    TrackShortOld,
    TrackTrailer,
    TrackWithAds,
    TrailerInfo,
    User,
    Value,
    Video,
    VideoSupplement,
    Vinyl,
    Wave,
    WaveAgent,
    WaveAgentEntity,
    WaveDefaultStation,
    WaveSettings,
    WaveSettingsBlock,
)

from . import (
    TestAccount,
    TestAdParams,
    TestAlbum,
    TestAlbumActionButton,
    TestAlert,
    TestAlertButton,
    TestArtist,
    TestArtistAbout,
    TestArtistClipItem,
    TestArtistConcerts,
    TestArtistDonationData,
    TestArtistDonationGoal,
    TestArtistDonationItem,
    TestArtistEvent,
    TestArtistInfo,
    TestArtistLink,
    TestArtistSkeleton,
    TestArtistTrailerStatus,
    TestAutoRenewable,
    TestBest,
    TestBlock,
    TestBlockEntity,
    TestBrand,
    TestCaseForms,
    TestChart,
    TestChartInfo,
    TestChartInfoMenuItem,
    TestClip,
    TestCombinedSession,
    TestCombinedSessionItem,
    TestCombinedSessionLanding,
    TestCombinedSessionQueueItem,
    TestConcert,
    TestConcertCashback,
    TestConcertDescription,
    TestConcertEventInfo,
    TestConcertFeedItem,
    TestConcertInfo,
    TestConcertLocation,
    TestConcertMinPrice,
    TestConcertSkeleton,
    TestConcertTabRange,
    TestContentRestrictions,
    TestContest,
    TestContext,
    TestCounts,
    TestCover,
    TestCoverDerivedColors,
    TestCredit,
    TestCustomWave,
    TestDay,
    TestDeactivation,
    TestDeprecation,
    TestDescription,
    TestDeviceCode,
    TestDiscreteScale,
    TestEnum,
    TestEvent,
    TestExperimentDetail,
    TestExperimentDetailValue,
    TestFade,
    TestFileDownloadInfo,
    TestForeignAgent,
    TestGeneratedPlaylist,
    TestGenerativeStream,
    TestGenerativeStreamData,
    TestGenerativeStreamFeedback,
    TestGenerativeStreamInfo,
    TestIcon,
    TestId,
    TestImages,
    TestInvocationInfo,
    TestLabel,
    TestLicenceTextPart,
    TestLink,
    TestLyrics,
    TestLyricsInfo,
    TestLyricsMajor,
    TestMajor,
    TestMetaData,
    TestMetatag,
    TestMetatagAlbums,
    TestMetatagArtists,
    TestMetatagLeaf,
    TestMetatagPlaylists,
    TestMetatagSortByValue,
    TestMetatagTitle,
    TestMetatagTree,
    TestMixLink,
    TestMusicHistoryContextFullModel,
    TestMusicHistoryItem,
    TestMusicHistoryItemId,
    TestMusicHistoryTab,
    TestNonAutoRenewable,
    TestNormalization,
    TestOAuthToken,
    TestOpenGraphData,
    TestOperator,
    TestPager,
    TestPassportPhone,
    TestPermissions,
    TestPersonalPlaylistsData,
    TestPin,
    TestPinData,
    TestPlayContext,
    TestPlayCounter,
    TestPlaylist,
    TestPlaylistAbsence,
    TestPlaylistAvailability,
    TestPlaylistId,
    TestPlaylistTrailer,
    TestPlus,
    TestPoetryLoverMatch,
    TestPrice,
    TestProduct,
    TestPromotion,
    TestR128,
    TestRatings,
    TestRenewableRemainder,
    TestRotorSeed,
    TestRotorSession,
    TestRotorSessionTracks,
    TestRotorSettings,
    TestSearchResult,
    TestSequence,
    TestSessionEvent,
    TestSessionFeedback,
    TestSessionFeedbacks,
    TestSessionPlayable,
    TestSettings,
    TestShot,
    TestShotData,
    TestShotType,
    TestSimilarEntityItem,
    TestSkeletonBlock,
    TestSkeletonBlockData,
    TestSkeletonSource,
    TestSkeletonTab,
    TestSkeletonViewAllAction,
    TestSmartPreviewParams,
    TestStation,
    TestStationData,
    TestStationResult,
    TestStats,
    TestStatus,
    TestSubscription,
    TestTag,
    TestTitle,
    TestTrack,
    TestTrackFullInfo,
    TestTrackId,
    TestTrackLyrics,
    TestTrackParameters,
    TestTrackPosition,
    TestTrackShort,
    TestTrackShortOld,
    TestTrackTrailer,
    TestTrackWithAds,
    TestTrailerInfo,
    TestUser,
    TestValue,
    TestVideo,
    TestVideoSupplement,
    TestVinyl,
    TestWave,
    TestWaveAgent,
    TestWaveAgentEntity,
    TestWaveDefaultStation,
    TestWaveSettingsBlock,
)

ResultItem = Union[
    Track,
    Artist,
    Album,
    Playlist,
    Video,
    GeneratedPlaylist,
    Promotion,
    ChartItem,
    PlayContext,
    MixLink,
    PersonalPlaylistsData,
    PlayContextsData,
    User,
]
SearchItem = Union[Track, Artist, Album, Playlist, Video, User]
BlockEntityData = Union[GeneratedPlaylist, Promotion, Album, Playlist, ChartItem, PlayContext, MixLink]
BlockData = Union[PersonalPlaylistsData, PlayContextsData]


def as_search_item(item: ResultItem) -> SearchItem:
    assert isinstance(item, (Track, Artist, Album, Playlist, Video, User))
    return item


def as_block_entity_data(item: ResultItem) -> BlockEntityData:
    assert isinstance(item, (GeneratedPlaylist, Promotion, Album, Playlist, ChartItem, PlayContext, MixLink))
    return item


def as_block_data(item: ResultItem) -> BlockData:
    assert isinstance(item, (PersonalPlaylistsData, PlayContextsData))
    return item


class ArtistFactory:
    def __init__(
        self,
        cover: Cover,
        counts: Counts,
        ratings: Ratings,
        link: Link,
        description: Description,
        content_restrictions: ContentRestrictions,
    ) -> None:
        self.cover = cover
        self.counts = counts
        self.ratings = ratings
        self.link = link
        self.description = description
        self.content_restrictions = content_restrictions

    def get(self, popular_tracks: List[Track], decomposed: Optional[List[Union[str, Artist]]] = None) -> Artist:
        return Artist(
            TestArtist.id,
            TestArtist.error,
            TestArtist.reason,
            TestArtist.name,
            self.cover,
            TestArtist.various,
            TestArtist.composer,
            TestArtist.genres,
            TestArtist.og_image,
            TestArtist.op_image,
            TestArtist.no_pictures_from_search,
            self.counts,
            TestArtist.available,
            self.ratings,
            [self.link],
            TestArtist.tickets_available,
            TestArtist.likes_count,
            popular_tracks,
            TestArtist.regions,
            decomposed,
            TestArtist.full_names,
            TestArtist.hand_made_description,
            self.description,
            TestArtist.countries,
            TestArtist.en_wikipedia_link,
            TestArtist.db_aliases,
            TestArtist.aliases,
            TestArtist.init_date,
            TestArtist.end_date,
            TestArtist.ya_money_id,
            TestArtist.disclaimers,
            self.content_restrictions,
        )


@pytest.fixture(scope='session')
def artist_factory(
    cover: Cover,
    counts: Counts,
    ratings: Ratings,
    link: Link,
    description: Description,
    content_restrictions: ContentRestrictions,
) -> ArtistFactory:
    return ArtistFactory(cover, counts, ratings, link, description, content_restrictions)


@pytest.fixture(scope='session')
def artist(
    artist_factory: ArtistFactory, track_without_artists_and_albums: Track, artist_decomposed: List[Union[str, Artist]]
) -> Artist:
    return artist_factory.get([track_without_artists_and_albums], artist_decomposed)


@pytest.fixture(scope='session')
def artist_without_nested_artist(artist_factory: ArtistFactory, track_without_artists_and_albums: Track) -> Artist:
    return artist_factory.get([track_without_artists_and_albums])


@pytest.fixture(scope='session')
def artist_without_tracks(artist_factory: ArtistFactory) -> Artist:
    return artist_factory.get([])


@pytest.fixture(scope='session')
def artist_decomposed(artist_without_nested_artist: Artist) -> List[Union[str, Artist]]:
    return [' & ', artist_without_nested_artist]


class TrackFactory:
    def __init__(
        self,
        major: Major,
        normalization: Normalization,
        user: User,
        meta_data: MetaData,
        poetry_lover_match: PoetryLoverMatch,
        r_128: R128,
        lyrics_info: LyricsInfo,
    ) -> None:
        self.major = major
        self.normalization = normalization
        self.user = user
        self.meta_data = meta_data
        self.poetry_lover_match = poetry_lover_match
        self.r_128 = r_128
        self.lyrics_info = lyrics_info

    def get(
        self, artists: List[Artist], albums: List[Album], track_without_nested_tracks: Optional[Track] = None
    ) -> Track:
        return Track(
            TestTrack.id,
            TestTrack.title,
            TestTrack.available,
            artists,
            albums,
            TestTrack.available_for_premium_users,
            TestTrack.lyrics_available,
            [self.poetry_lover_match],
            TestTrack.best,
            TestTrack.real_id,
            TestTrack.og_image,
            TestTrack.type,
            TestTrack.cover_uri,
            self.major,
            TestTrack.duration_ms,
            TestTrack.storage_dir,
            TestTrack.file_size,
            track_without_nested_tracks,
            track_without_nested_tracks,
            self.normalization,
            TestTrack.error,
            TestTrack.can_publish,
            TestTrack.state,
            TestTrack.desired_visibility,
            TestTrack.filename,
            self.user,
            self.meta_data,
            TestTrack.regions,
            TestTrack.available_as_rbt,
            TestTrack.content_warning,
            TestTrack.explicit,
            TestTrack.preview_duration_ms,
            TestTrack.available_full_without_permission,
            TestTrack.version,
            TestTrack.remember_position,
            TestTrack.background_video_uri,
            TestTrack.short_description,
            TestTrack.is_suitable_for_children,
            TestTrack.track_source,
            TestTrack.available_for_options,
            self.r_128,
            self.lyrics_info,
            TestTrack.track_sharing_flag,
        )


@pytest.fixture(scope='session')
def track_factory(
    major: Major,
    normalization: Normalization,
    user: User,
    meta_data: MetaData,
    poetry_lover_match: PoetryLoverMatch,
    r_128: R128,
    lyrics_info: LyricsInfo,
) -> TrackFactory:
    return TrackFactory(major, normalization, user, meta_data, poetry_lover_match, r_128, lyrics_info)


@pytest.fixture(scope='session')
def track(track_factory: TrackFactory, artist: Artist, album: Album, track_without_nested_tracks: Track) -> Track:
    return track_factory.get([artist], [album], track_without_nested_tracks)


@pytest.fixture(scope='session')
def track_without_artists(track_factory: TrackFactory, album: Album) -> Track:
    return track_factory.get([], [album])


@pytest.fixture(scope='session')
def track_without_albums(track_factory: TrackFactory, artist: Artist) -> Track:
    return track_factory.get([artist], [])


@pytest.fixture(scope='session')
def track_without_artists_and_albums(track_factory: TrackFactory) -> Track:
    return track_factory.get([], [])


@pytest.fixture(scope='session')
def track_without_nested_tracks(artist: Artist, album: Album, track_factory: TrackFactory) -> Track:
    return track_factory.get([artist], [album])


@pytest.fixture(scope='session')
def lyrics_major() -> LyricsMajor:
    return LyricsMajor(
        TestLyricsMajor.id,
        TestLyricsMajor.name,
        TestLyricsMajor.pretty_name,
    )


@pytest.fixture(scope='session')
def track_lyrics(lyrics_major: LyricsMajor) -> TrackLyrics:
    return TrackLyrics(
        TestTrackLyrics.download_url,
        TestTrackLyrics.lyric_id,
        TestTrackLyrics.external_lyric_id,
        TestTrackLyrics.writer,
        lyrics_major,
    )


@pytest.fixture(scope='session')
def album_action_button() -> AlbumActionButton:
    return AlbumActionButton(
        TestAlbumActionButton.text,
        TestAlbumActionButton.url,
        TestAlbumActionButton.color,
    )


class AlbumFactory:
    def __init__(
        self,
        label: Union[Label, str],
        track_position: TrackPosition,
        album_action_button: AlbumActionButton,
        cover: Cover,
        cover_derived_colors: CoverDerivedColors,
    ) -> None:
        self.labels: Union[List[Label], List[str]]
        if isinstance(label, Label):
            self.labels = [label]
        else:
            self.labels = [label]
        self.track_position = track_position
        self.album_action_button = album_action_button
        self.cover = cover
        self.cover_derived_colors = cover_derived_colors

    def get(
        self,
        artists: List[Artist],
        volumes: List[List[Track]],
        albums: Optional[List[Album]] = None,
        deprecation: Optional[Deprecation] = None,
    ) -> Album:
        return Album(
            TestAlbum.id,
            TestAlbum.error,
            TestAlbum.title,
            TestAlbum.track_count,
            artists,
            self.labels,
            TestAlbum.available,
            TestAlbum.available_for_premium_users,
            TestAlbum.version,
            TestAlbum.cover_uri,
            TestAlbum.content_warning,
            TestAlbum.original_release_year,
            TestAlbum.genre,
            TestAlbum.text_color,
            TestAlbum.short_description,
            TestAlbum.description,
            TestAlbum.is_premiere,
            TestAlbum.is_banner,
            TestAlbum.meta_type,
            TestAlbum.storage_dir,
            TestAlbum.og_image,
            TestAlbum.buy,
            TestAlbum.recent,
            TestAlbum.very_important,
            TestAlbum.available_for_mobile,
            TestAlbum.available_partially,
            TestAlbum.bests,
            albums if albums is not None else [],
            TestAlbum.prerolls,
            volumes,
            TestAlbum.year,
            TestAlbum.release_date,
            TestAlbum.type,
            self.track_position,
            TestAlbum.regions,
            TestAlbum.available_as_rbt,
            TestAlbum.lyrics_available,
            TestAlbum.remember_position,
            albums,
            TestAlbum.duration_ms,
            TestAlbum.explicit,
            TestAlbum.start_date,
            TestAlbum.likes_count,
            deprecation,
            TestAlbum.available_regions,
            TestAlbum.available_for_options,
            disclaimers=TestAlbum.disclaimers,
            action_button=self.album_action_button,
            cover=self.cover,
            derived_colors=self.cover_derived_colors,
            meta_tag_id=TestAlbum.meta_tag_id,
            child_content=TestAlbum.child_content,
        )


@pytest.fixture(scope='session')
def album_factory(
    label: Union[Label, str],
    track_position: TrackPosition,
    album_action_button: AlbumActionButton,
    cover: Cover,
    cover_derived_colors: CoverDerivedColors,
) -> AlbumFactory:
    return AlbumFactory(label, track_position, album_action_button, cover, cover_derived_colors)


@pytest.fixture(scope='session')
def album(
    album_factory: AlbumFactory,
    artist_without_tracks: Artist,
    track_without_albums: Track,
    album_without_nested_albums: Album,
    deprecation: Deprecation,
) -> Album:
    return album_factory.get(
        [artist_without_tracks], [[track_without_albums]], [album_without_nested_albums], deprecation
    )


@pytest.fixture(scope='session')
def album_without_tracks(album_factory: AlbumFactory, artist_without_tracks: Artist) -> Album:
    return album_factory.get([artist_without_tracks], [])


@pytest.fixture(scope='session')
def album_without_nested_albums(
    album_factory: AlbumFactory, artist_without_tracks: Artist, track_without_albums: Track
) -> Album:
    return album_factory.get([artist_without_tracks], [[track_without_albums]])


class PlaylistFactory:
    def __init__(
        self,
        user: User,
        cover: Cover,
        made_for: MadeFor,
        track_short: TrackShort,
        play_counter: PlayCounter,
        playlist_absence: PlaylistAbsence,
        artist: Artist,
        track_id: TrackId,
        contest: Contest,
        open_graph_data: OpenGraphData,
        brand: Brand,
        custom_wave: CustomWave,
        pager: Pager,
    ) -> None:
        self.user = user
        self.cover = cover
        self.made_for = made_for
        self.track_short = track_short
        self.play_counter = play_counter
        self.playlist_absence = playlist_absence
        self.artist = artist
        self.track_id = track_id
        self.contest = contest
        self.open_graph_data = open_graph_data
        self.brand = brand
        self.custom_wave = custom_wave
        self.pager = pager

    def get(self, similar_playlists: List[Playlist], last_owner_playlists: List[Playlist]) -> Playlist:
        return Playlist(
            self.user,
            self.cover,
            self.made_for,
            self.play_counter,
            self.playlist_absence,
            TestPlaylist.uid,
            TestPlaylist.kind,
            TestPlaylist.title,
            TestPlaylist.track_count,
            TestPlaylist.tags,
            TestPlaylist.revision,
            TestPlaylist.snapshot,
            TestPlaylist.visibility,
            TestPlaylist.collective,
            TestPlaylist.url_part,
            TestPlaylist.created,
            TestPlaylist.modified,
            TestPlaylist.available,
            TestPlaylist.is_banner,
            TestPlaylist.is_premiere,
            TestPlaylist.duration_ms,
            TestPlaylist.og_image,
            TestPlaylist.og_title,
            TestPlaylist.og_description,
            TestPlaylist.image,
            self.cover,
            self.contest,
            TestPlaylist.background_color,
            TestPlaylist.text_color,
            TestPlaylist.id_for_from,
            TestPlaylist.dummy_description,
            TestPlaylist.dummy_page_description,
            self.cover,
            self.cover,
            self.open_graph_data,
            self.brand,
            TestPlaylist.metrika_id,
            TestPlaylist.coauthors,
            [self.artist],
            [self.track_id],
            [self.track_short],
            TestPlaylist.prerolls,
            TestPlaylist.likes_count,
            similar_playlists,
            last_owner_playlists,
            TestPlaylist.generated_playlist_type,
            TestPlaylist.animated_cover_uri,
            TestPlaylist.ever_played,
            TestPlaylist.description,
            TestPlaylist.description_formatted,
            TestPlaylist.playlist_uuid,
            TestPlaylist.type,
            TestPlaylist.ready,
            TestPlaylist.is_for_from,
            TestPlaylist.regions,
            self.custom_wave,
            self.pager,
        )


@pytest.fixture(scope='session')
def playlist_factory(
    user: User,
    cover: Cover,
    made_for: MadeFor,
    track_short: TrackShort,
    play_counter: PlayCounter,
    playlist_absence: PlaylistAbsence,
    artist: Artist,
    track_id: TrackId,
    contest: Contest,
    open_graph_data: OpenGraphData,
    brand: Brand,
    custom_wave: CustomWave,
    pager: Pager,
) -> PlaylistFactory:
    return PlaylistFactory(
        user,
        cover,
        made_for,
        track_short,
        play_counter,
        playlist_absence,
        artist,
        track_id,
        contest,
        open_graph_data,
        brand,
        custom_wave,
        pager,
    )


@pytest.fixture(scope='session')
def playlist(playlist_factory: PlaylistFactory, playlist_without_nested_playlists: Playlist) -> Playlist:
    return playlist_factory.get([playlist_without_nested_playlists], [playlist_without_nested_playlists])


@pytest.fixture(scope='session')
def playlist_without_nested_playlists(playlist_factory: PlaylistFactory) -> Playlist:
    return playlist_factory.get([], [])


@pytest.fixture(scope='session')
def generated_playlist(playlist: Playlist) -> GeneratedPlaylist:
    return GeneratedPlaylist(
        TestGeneratedPlaylist.type,
        TestGeneratedPlaylist.ready,
        TestGeneratedPlaylist.notify,
        playlist,
        TestGeneratedPlaylist.description,
        TestGeneratedPlaylist.preview_description,
    )


@pytest.fixture(scope='session')
def client() -> Client:
    return Client()


@pytest.fixture(scope='session')
def device_code() -> DeviceCode:
    return DeviceCode(
        TestDeviceCode.device_code,
        TestDeviceCode.user_code,
        TestDeviceCode.verification_url,
        TestDeviceCode.expires_in,
        TestDeviceCode.interval,
    )


@pytest.fixture(scope='session')
def oauth_token() -> OAuthToken:
    return OAuthToken(
        TestOAuthToken.access_token,
        TestOAuthToken.refresh_token,
        TestOAuthToken.expires_in,
        TestOAuthToken.token_type,
    )


@pytest.fixture(scope='session')
def tag() -> Tag:
    return Tag(TestTag.id_, TestTag.value, TestTag.name, TestTag.og_description, TestTag.og_image)


@pytest.fixture(scope='session')
def brand() -> Brand:
    return Brand(
        TestBrand.image,
        TestBrand.background,
        TestBrand.reference,
        TestBrand.pixels,
        TestBrand.theme,
        TestBrand.playlist_theme,
        TestBrand.button,
    )


@pytest.fixture(scope='session')
def track_with_ads(track: Track) -> TrackWithAds:
    return TrackWithAds(TestTrackWithAds.type, track)


@pytest.fixture(scope='session')
def day(event: Event, track_with_ads: TrackWithAds, track: Track) -> Day:
    return Day(TestDay.day, [event], [track_with_ads], [track])


@pytest.fixture(scope='session')
def track_short() -> TrackShort:
    return TrackShort(TestTrackShort.id, TestTrackShort.timestamp, TestTrackShort.album_id)


@pytest.fixture(scope='session')
def track_short_old(track_id: TrackId) -> TrackShortOld:
    return TrackShortOld(track_id, TestTrackShortOld.timestamp)


@pytest.fixture(scope='session')
def video() -> Video:
    return Video(
        TestVideo.title,
        TestVideo.cover,
        TestVideo.embed_url,
        TestVideo.provider,
        TestVideo.provider_video_id,
        TestVideo.youtube_url,
        TestVideo.thumbnail_url,
        TestVideo.duration,
        TestVideo.text,
        TestVideo.html_auto_play_video_player,
        TestVideo.regions,
    )


@pytest.fixture(scope='session')
def vinyl() -> Vinyl:
    return Vinyl(
        TestVinyl.url,
        TestVinyl.title,
        TestVinyl.year,
        TestVinyl.price,
        TestVinyl.media,
        TestVinyl.offer_id,
        TestVinyl.artist_ids,
        TestVinyl.picture,
    )


@pytest.fixture(scope='session')
def play_context(track_short_old: TrackShortOld) -> PlayContext:
    return PlayContext(
        TestPlayContext.client_, TestPlayContext.context, TestPlayContext.context_item, [track_short_old]
    )


@pytest.fixture(scope='session')
def play_contexts_data(track_short_old: TrackShortOld) -> PlayContextsData:
    return PlayContextsData([track_short_old])


@pytest.fixture(scope='session')
def enum(value: Value) -> Enum:
    return Enum(TestEnum.type, TestEnum.name, [value])


@pytest.fixture(scope='session')
def icon() -> Icon:
    return Icon(TestIcon.background_color, TestIcon.image_url)


@pytest.fixture(scope='session')
def content_restrictions() -> ContentRestrictions:
    return ContentRestrictions(
        TestContentRestrictions.available,
        TestContentRestrictions.disclaimers,
    )


@pytest.fixture(scope='session')
def cover_derived_colors() -> CoverDerivedColors:
    return CoverDerivedColors(
        TestCoverDerivedColors.average,
        TestCoverDerivedColors.wave_text,
        TestCoverDerivedColors.mini_player,
        TestCoverDerivedColors.accent,
    )


@pytest.fixture(scope='session')
def cover(cover_derived_colors: CoverDerivedColors) -> Cover:
    return Cover(
        TestCover.type,
        TestCover.uri,
        TestCover.items_uri,
        TestCover.dir,
        TestCover.version,
        TestCover.custom,
        TestCover.is_custom,
        TestCover.copyright_name,
        TestCover.copyright_cline,
        TestCover.prefix,
        TestCover.error,
        TestCover.color,
        cover_derived_colors,
    )


@pytest.fixture(scope='session')
def concert_min_price() -> ConcertMinPrice:
    return ConcertMinPrice(
        TestConcertMinPrice.value,
        TestConcertMinPrice.currency,
        TestConcertMinPrice.currency_symbol,
    )


@pytest.fixture(scope='session')
def concert_cashback() -> ConcertCashback:
    return ConcertCashback(
        TestConcertCashback.title,
        TestConcertCashback.value_percent,
    )


@pytest.fixture(scope='session')
def concert_event_info() -> ConcertEventInfo:
    return ConcertEventInfo(
        TestConcertEventInfo.type,
    )


@pytest.fixture(scope='session')
def concert(
    concert_min_price: ConcertMinPrice,
    concert_cashback: ConcertCashback,
    concert_event_info: ConcertEventInfo,
    cover: Cover,
) -> Concert:
    return Concert(
        TestConcert.id,
        TestConcert.images,
        TestConcert.image_url,
        TestConcert.concert_title,
        TestConcert.afisha_url,
        TestConcert.city,
        TestConcert.place,
        TestConcert.address,
        TestConcert.datetime,
        TestConcert.content_rating,
        concert_min_price,
        concert_cashback,
        concert_event_info,
        cover,
        TestConcert.data_session_id,
    )


@pytest.fixture(scope='session')
def artist_concerts(concert: Concert) -> ArtistConcerts:
    return ArtistConcerts(
        TestArtistConcerts.artist_title,
        [concert],
    )


@pytest.fixture(scope='session')
def concert_description() -> ConcertDescription:
    return ConcertDescription(
        TestConcertDescription.text,
        TestConcertDescription.source,
    )


@pytest.fixture(scope='session')
def concert_location() -> ConcertLocation:
    return ConcertLocation(
        TestConcertLocation.id,
        TestConcertLocation.name,
    )


@pytest.fixture(scope='session')
def concert_locations(concert_location: ConcertLocation) -> ConcertLocations:
    return ConcertLocations(
        [concert_location],
    )


@pytest.fixture(scope='session')
def concert_tab_range() -> ConcertTabRange:
    return ConcertTabRange(
        TestConcertTabRange.offset,
        TestConcertTabRange.limit,
    )


@pytest.fixture(scope='session')
def concert_tab_config_data(concert_tab_range: ConcertTabRange) -> ConcertTabConfigData:
    return ConcertTabConfigData(
        concert_tab_range,
        concert_tab_range,
    )


@pytest.fixture(scope='session')
def concert_tab_config(concert_tab_config_data: ConcertTabConfigData) -> ConcertTabConfig:
    return ConcertTabConfig(
        concert_tab_config_data,
    )


@pytest.fixture(scope='session')
def concert_feed_item_data(concert: Concert, concert_min_price: ConcertMinPrice) -> ConcertFeedItemData:
    return ConcertFeedItemData(
        concert,
        concert_min_price,
    )


@pytest.fixture(scope='session')
def concert_feed_item(concert_feed_item_data: ConcertFeedItemData) -> ConcertFeedItem:
    return ConcertFeedItem(
        TestConcertFeedItem.type,
        concert_feed_item_data,
    )


@pytest.fixture(scope='session')
def concert_feed(concert_feed_item: ConcertFeedItem) -> ConcertFeed:
    return ConcertFeed(
        [concert_feed_item],
    )


@pytest.fixture(scope='session')
def concert_info(
    concert: Concert, concert_min_price: ConcertMinPrice, cover: Cover, concert_description: ConcertDescription
) -> ConcertInfo:
    return ConcertInfo(
        concert,
        concert_min_price,
        [cover],
        concert_description,
        TestConcertInfo.lead_artist_id,
    )


@pytest.fixture(scope='session')
def concert_skeleton(skeleton_block: SkeletonBlock) -> ConcertSkeleton:
    return ConcertSkeleton(
        TestConcertSkeleton.id,
        TestConcertSkeleton.title,
        [skeleton_block],
    )


@pytest.fixture(scope='session')
def open_graph_data(cover: Cover) -> OpenGraphData:
    return OpenGraphData(TestOpenGraphData.title, TestOpenGraphData.description, cover)


@pytest.fixture(scope='session')
def meta_data() -> MetaData:
    return MetaData(
        TestMetaData.album,
        TestMetaData.volume,
        TestMetaData.year,
        TestMetaData.number,
        TestMetaData.genre,
        TestMetaData.lyricist,
        TestMetaData.version,
        TestMetaData.composer,
    )


@pytest.fixture(scope='session')
def licence_text_part() -> LicenceTextPart:
    return LicenceTextPart(TestLicenceTextPart.text, TestLicenceTextPart.url)


@pytest.fixture(scope='session')
def link() -> Link:
    return Link(TestLink.title, TestLink.href, TestLink.type, TestLink.social_network)


@pytest.fixture(scope='session')
def invocation_info() -> InvocationInfo:
    return InvocationInfo(
        TestInvocationInfo.hostname,
        TestInvocationInfo.req_id,
        TestInvocationInfo.exec_duration_millis,
        TestInvocationInfo.app_name,
    )


@pytest.fixture(scope='session')
def settings(product: Product, price: Price) -> Settings:
    return Settings([product], [product], TestSettings.web_payment_url, TestSettings.promo_codes_enabled, price)


@pytest.fixture(scope='session')
def counts() -> Counts:
    return Counts(TestCounts.tracks, TestCounts.direct_albums, TestCounts.also_albums, TestCounts.also_tracks)


@pytest.fixture(scope='session')
def description() -> Description:
    return Description(TestDescription.text, TestDescription.uri)


@pytest.fixture(scope='session')
def deprecation() -> Deprecation:
    return Deprecation(TestDeprecation.target_album_id, TestDeprecation.status, TestDeprecation.done)


@pytest.fixture(scope='session')
def pager() -> Pager:
    return Pager(TestPager.total, TestPager.page, TestPager.per_page)


@pytest.fixture(scope='session')
def clip(artist: Artist, cover: Cover, content_restrictions: ContentRestrictions) -> Clip:
    return Clip(
        clip_id=TestClip.clip_id,
        title=TestClip.title,
        version=TestClip.version,
        player_id=TestClip.player_id,
        uuid=TestClip.uuid,
        thumbnail=TestClip.thumbnail,
        preview_url=TestClip.preview_url,
        duration=TestClip.duration,
        track_ids=TestClip.track_ids,
        artists=[artist],
        disclaimers=TestClip.disclaimers,
        explicit=TestClip.explicit,
        cover=cover,
        content_restrictions=content_restrictions,
    )


@pytest.fixture(scope='session')
def clips_will_like(clip: Clip, pager: Pager) -> ClipsWillLike:
    return ClipsWillLike(
        clips=[clip],
        pager=pager,
    )


@pytest.fixture(scope='session')
def artist_event(artist: Artist, track: Track) -> ArtistEvent:
    return ArtistEvent(artist, [track], [artist], TestArtistEvent.subscribed)


@pytest.fixture(scope='session')
def album_event(album: Album, track: Track) -> AlbumEvent:
    return AlbumEvent(album, [track])


@pytest.fixture(scope='session')
def video_supplement() -> VideoSupplement:
    return VideoSupplement(
        TestVideoSupplement.cover,
        TestVideoSupplement.provider,
        TestVideoSupplement.title,
        TestVideoSupplement.provider_video_id,
        TestVideoSupplement.url,
        TestVideoSupplement.embed_url,
        TestVideoSupplement.embed,
    )


@pytest.fixture(scope='session')
def ratings() -> Ratings:
    return Ratings(TestRatings.month, TestRatings.week, TestRatings.day)


@pytest.fixture(scope='session')
def made_for(user: User, case_forms: CaseForms) -> MadeFor:
    return MadeFor(user, case_forms)


@pytest.fixture(scope='session')
def play_counter() -> PlayCounter:
    return PlayCounter(TestPlayCounter.value, TestPlayCounter.description, TestPlayCounter.updated)


@pytest.fixture(scope='session')
def playlist_absence() -> PlaylistAbsence:
    return PlaylistAbsence(TestPlaylistAbsence.kind, TestPlaylistAbsence.reason)


@pytest.fixture(scope='session')
def context() -> Context:
    return Context(TestContext.type_, TestContext.id_, TestContext.description)


@pytest.fixture(scope='session')
def case_forms() -> CaseForms:
    return CaseForms(
        TestCaseForms.nominative,
        TestCaseForms.genitive,
        TestCaseForms.dative,
        TestCaseForms.accusative,
        TestCaseForms.instrumental,
        TestCaseForms.prepositional,
    )


@pytest.fixture(scope='session')
def lyrics() -> Lyrics:
    return Lyrics(
        TestLyrics.id,
        TestLyrics.lyrics,
        TestLyrics.full_lyrics,
        TestLyrics.has_rights,
        TestLyrics.show_translation,
        TestLyrics.text_language,
        TestLyrics.url,
    )


@pytest.fixture(scope='session')
def poetry_lover_match() -> PoetryLoverMatch:
    return PoetryLoverMatch(TestPoetryLoverMatch.begin, TestPoetryLoverMatch.end, TestPoetryLoverMatch.line)


@pytest.fixture(scope='session')
def images() -> Images:
    return Images(TestImages._208x208, TestImages._300x300)


@pytest.fixture(scope='session')
def normalization() -> Normalization:
    return Normalization(TestNormalization.gain, TestNormalization.peak)


@pytest.fixture(scope='session')
def mix_link() -> MixLink:
    return MixLink(
        TestMixLink.title,
        TestMixLink.url,
        TestMixLink.url_scheme,
        TestMixLink.text_color,
        TestMixLink.background_color,
        TestMixLink.background_image_uri,
        TestMixLink.cover_white,
        TestMixLink.cover_uri,
    )


@pytest.fixture(scope='session')
def title() -> Title:
    return Title(TestTitle.title, TestTitle.full_title)


@pytest.fixture(scope='session')
def personal_playlists_data() -> PersonalPlaylistsData:
    return PersonalPlaylistsData(TestPersonalPlaylistsData.is_wizard_passed)


@pytest.fixture(scope='session')
def promotion() -> Promotion:
    return Promotion(
        TestPromotion.promo_id,
        TestPromotion.title,
        TestPromotion.subtitle,
        TestPromotion.heading,
        TestPromotion.url,
        TestPromotion.url_scheme,
        TestPromotion.text_color,
        TestPromotion.gradient,
        TestPromotion.image,
    )


@pytest.fixture(scope='session')
def discrete_scale(value: Value) -> DiscreteScale:
    return DiscreteScale(TestDiscreteScale.type, TestDiscreteScale.name, value, value)


@pytest.fixture(scope='session')
def major() -> Major:
    return Major(TestMajor.id, TestMajor.name)


@pytest.fixture(scope='session')
def permissions() -> Permissions:
    return Permissions(TestPermissions.until, TestPermissions.values, TestPermissions.default)


@pytest.fixture(scope='session')
def auto_renewable(product: Product, user: User) -> AutoRenewable:
    return AutoRenewable(
        TestAutoRenewable.expires,
        TestAutoRenewable.vendor,
        TestAutoRenewable.vendor_help_url,
        product,
        TestAutoRenewable.finished,
        user,
        TestAutoRenewable.product_id,
        TestAutoRenewable.order_id,
    )


@pytest.fixture(scope='session')
def passport_phone() -> PassportPhone:
    return PassportPhone(TestPassportPhone.phone)


@pytest.fixture(scope='session')
def renewable_remainder() -> RenewableRemainder:
    return RenewableRemainder(TestRenewableRemainder.days)


@pytest.fixture(scope='session')
def user() -> User:
    return User(
        TestUser.uid,
        TestUser.login,
        TestUser.name,
        TestUser.display_name,
        TestUser.full_name,
        TestUser.sex,
        TestUser.verified,
        TestUser.regions,
    )


@pytest.fixture(scope='session')
def account(passport_phone: PassportPhone) -> Account:
    return Account(
        TestAccount.now,
        TestAccount.service_available,
        TestAccount.region,
        TestAccount.uid,
        TestAccount.login,
        TestAccount.full_name,
        TestAccount.second_name,
        TestAccount.first_name,
        TestAccount.display_name,
        TestAccount.hosted_user,
        TestAccount.birthday,
        [passport_phone],
        TestAccount.registered_at,
        TestAccount.has_info_for_app_metrica,
        TestAccount.child,
        TestAccount.region_code,
        TestAccount.non_owner_family_member,
    )


@pytest.fixture(scope='session')
def plus() -> Plus:
    return Plus(TestPlus.has_plus, TestPlus.is_tutorial_completed, TestPlus.migrated)


@pytest.fixture(scope='session')
def price() -> Price:
    return Price(TestPrice.amount, TestPrice.currency)


@pytest.fixture(scope='session')
def subscription(
    renewable_remainder: RenewableRemainder,
    auto_renewable: AutoRenewable,
    operator: Operator,
    non_auto_renewable: NonAutoRenewable,
) -> Subscription:
    return Subscription(
        auto_renewable=[auto_renewable],
        family_auto_renewable=[auto_renewable],
        non_auto_renewable_remainder=renewable_remainder,
        had_any_subscription=TestSubscription.had_any_subscription,
        operator=[operator],
        non_auto_renewable=non_auto_renewable,
        can_start_trial=TestSubscription.can_start_trial,
        mcdonalds=TestSubscription.mcdonalds,
        end=TestSubscription.end,
    )


@pytest.fixture(scope='session')
def non_auto_renewable() -> NonAutoRenewable:
    return NonAutoRenewable(TestNonAutoRenewable.start, TestNonAutoRenewable.end)


@pytest.fixture(scope='session')
def deactivation() -> Deactivation:
    return Deactivation(TestDeactivation.method, TestDeactivation.instructions)


@pytest.fixture(scope='session')
def operator(deactivation: Deactivation) -> Operator:
    return Operator(
        TestOperator.product_id,
        TestOperator.phone,
        TestOperator.payment_regularity,
        [deactivation],
        TestOperator.title,
        TestOperator.suspended,
    )


@pytest.fixture(scope='session')
def rotor_settings() -> RotorSettings:
    return RotorSettings(
        TestRotorSettings.language,
        TestRotorSettings.diversity,
        TestRotorSettings.mood,
        TestRotorSettings.energy,
        TestRotorSettings.mood_energy,
    )


@pytest.fixture(scope='session')
def product(price: Price, licence_text_part: LicenceTextPart) -> Product:
    return Product(
        TestProduct.product_id,
        TestProduct.type,
        TestProduct.duration,
        TestProduct.trial_duration,
        TestProduct.feature,
        TestProduct.debug,
        TestProduct.plus,
        price,
        TestProduct.common_period_duration,
        TestProduct.cheapest,
        TestProduct.title,
        TestProduct.family_sub,
        TestProduct.fb_image,
        TestProduct.fb_name,
        TestProduct.family,
        TestProduct.features,
        TestProduct.description,
        TestProduct.available,
        TestProduct.trial_available,
        TestProduct.trial_period_duration,
        TestProduct.intro_period_duration,
        price,
        TestProduct.start_period_duration,
        price,
        [licence_text_part],
        TestProduct.vendor_trial_available,
        TestProduct.button_text,
        TestProduct.button_additional_text,
        TestProduct.payment_method_types,
    )


@pytest.fixture(scope='session')
def playlist_id() -> PlaylistId:
    return PlaylistId(TestPlaylistId.uid, TestPlaylistId.kind)


@pytest.fixture(scope='session')
def contest() -> Contest:
    return Contest(
        TestContest.contest_id, TestContest.status, TestContest.can_edit, TestContest.sent, TestContest.withdrawn
    )


@pytest.fixture(scope='session', params=[True, False])
def label(request: pytest.FixtureRequest, link: Link) -> Union[Label, str]:
    if request.param:
        return Label(
            TestLabel.id,
            TestLabel.name,
            TestLabel.description,
            TestLabel.description_formatted,
            TestLabel.image,
            [link],
            TestLabel.type,
        )

    return TestLabel.another_representation_of_label


@pytest.fixture(scope='session')
def track_position() -> TrackPosition:
    return TrackPosition(TestTrackPosition.volume, TestTrackPosition.index)


@pytest.fixture(scope='session')
def status(
    account: Account,
    permissions: Permissions,
    subscription: Subscription,
    plus: Plus,
    station_data: StationData,
    alert: Alert,
) -> Status:
    return Status(
        account,
        permissions,
        TestStatus.advertisement,
        subscription,
        TestStatus.cache_limit,
        TestStatus.subeditor,
        TestStatus.subeditor_level,
        plus,
        TestStatus.default_email,
        TestStatus.skips_per_hour,
        TestStatus.station_exists,
        station_data,
        alert,
        TestStatus.premium_region,
        TestStatus.experiment,
        TestStatus.pretrial_active,
        TestStatus.userhash,
        TestStatus.has_options,
    )


@pytest.fixture(scope='session')
def station_data() -> StationData:
    return StationData(TestStationData.name)


@pytest.fixture(scope='session')
def alert_button() -> AlertButton:
    return AlertButton(TestAlertButton.text, TestAlertButton.bg_color, TestAlertButton.text_color, TestAlertButton.uri)


@pytest.fixture(scope='session')
def alert(alert_button: AlertButton) -> Alert:
    return Alert(
        TestAlert.alert_id,
        TestAlert.text,
        TestAlert.bg_color,
        TestAlert.text_color,
        TestAlert.alert_type,
        alert_button,
        TestAlert.close_button,
    )


@pytest.fixture(scope='session')
def chart(track_id: TrackId) -> Chart:
    return Chart(
        TestChart.position, TestChart.progress, TestChart.listeners, TestChart.shift, TestChart.bg_color, track_id
    )


@pytest.fixture(scope='session')
def event(track: Track, artist_event: ArtistEvent, album_event: AlbumEvent) -> Event:
    return Event(
        TestEvent.id,
        TestEvent.type,
        TestEvent.type_for_from,
        TestEvent.title,
        [track],
        [artist_event],
        [album_event],
        TestEvent.message,
        TestEvent.device,
        TestEvent.tracks_count,
        TestEvent.genre,
    )


@pytest.fixture(scope='session')
def chart_info_menu_item() -> ChartInfoMenuItem:
    return ChartInfoMenuItem(TestChartInfoMenuItem.title, TestChartInfoMenuItem.url, TestChartInfoMenuItem.selected)


@pytest.fixture(scope='session')
def chart_info_menu(chart_info_menu_item: ChartInfoMenuItem) -> ChartInfoMenu:
    return ChartInfoMenu([chart_info_menu_item])


@pytest.fixture(scope='session')
def chart_info(playlist: Playlist, chart_info_menu: ChartInfoMenu) -> ChartInfo:
    return ChartInfo(
        TestChartInfo.id,
        TestChartInfo.type,
        TestChartInfo.type_for_from,
        TestChartInfo.title,
        chart_info_menu,
        playlist,
        TestChartInfo.chart_description,
    )


@pytest.fixture(scope='session')
def track_id() -> TrackId:
    return TrackId(TestTrackId.id, TestTrackId.track_id, TestTrackId.album_id, TestTrackId.from_)


@pytest.fixture(scope='session')
def value() -> Value:
    return Value(TestValue.value, TestValue.name, TestValue.image_url, TestValue.serialized_seed, TestValue.unspecified)


@pytest.fixture(scope='session')
def id_() -> Id:
    return Id(TestId.type, TestId.tag)


@pytest.fixture(scope='session')
def sequence(track: Track, track_parameters: TrackParameters) -> Sequence:
    return Sequence(TestSequence.type, track, TestSequence.liked, track_parameters)


@pytest.fixture(scope='session')
def station(id_: Id, icon: Icon, restrictions: Restrictions) -> Station:
    return Station(
        id_,
        TestStation.name,
        icon,
        icon,
        icon,
        TestStation.id_for_from,
        restrictions,
        restrictions,
        TestStation.full_image_url,
        TestStation.mts_full_image_url,
        id_,
        TestStation.special_context,
        TestStation.listeners,
        TestStation.login,
        TestStation.full_name,
        TestStation.display_name,
        TestStation.visibility,
    )


@pytest.fixture(scope='session')
def shot_type() -> ShotType:
    return ShotType(TestShotType.id, TestShotType.title)


@pytest.fixture(scope='session')
def shot_data(shot_type: ShotType) -> ShotData:
    return ShotData(TestShotData.cover_uri, TestShotData.mds_url, TestShotData.shot_text, shot_type)


@pytest.fixture(scope='session')
def shot(shot_data: ShotData) -> Shot:
    return Shot(TestShot.order, TestShot.played, shot_data, TestShot.shot_id, TestShot.status)


@pytest.fixture(scope='session')
def chart_item(track: Track, chart: Chart) -> ChartItem:
    return ChartItem(track, chart)


@pytest.fixture(scope='session')
def station_result(station: Station, rotor_settings: RotorSettings, ad_params: AdParams) -> StationResult:
    return StationResult(
        station,
        rotor_settings,
        rotor_settings,
        ad_params,
        TestStationResult.explanation,
        TestStationResult.prerolls,
        TestStationResult.rup_title,
        TestStationResult.rup_description,
        TestStationResult.custom_name,
    )


@pytest.fixture(scope='session')
def ad_params() -> AdParams:
    return AdParams(
        TestAdParams.partner_id,
        TestAdParams.category_id,
        TestAdParams.page_ref,
        TestAdParams.target_ref,
        TestAdParams.other_params,
        TestAdParams.ad_volume,
        TestAdParams.genre_id,
        TestAdParams.genre_name,
    )


@pytest.fixture(scope='session')
def restrictions(enum: Enum, discrete_scale: DiscreteScale) -> Restrictions:
    return Restrictions(enum, enum, discrete_scale, discrete_scale, enum)


@pytest.fixture(scope='session')
def results(
    track: Track,
    artist: Artist,
    album: Album,
    playlist: Playlist,
    video: Video,
    generated_playlist: GeneratedPlaylist,
    promotion: Promotion,
    chart_item: ChartItem,
    play_context: PlayContext,
    mix_link: MixLink,
    personal_playlists_data: PersonalPlaylistsData,
    play_contexts_data: PlayContextsData,
    user: User,
) -> Dict[int, ResultItem]:
    return {
        1: track,
        2: artist,
        3: album,
        4: playlist,
        5: video,
        6: generated_playlist,
        7: promotion,
        8: chart_item,
        9: play_context,
        10: mix_link,
        11: personal_playlists_data,
        12: play_contexts_data,
        13: user,
        14: album,
        15: track,
    }


@pytest.fixture(scope='session')
def types() -> Dict[int, str]:
    return {
        1: 'track',
        2: 'artist',
        3: 'album',
        4: 'playlist',
        5: 'video',
        6: 'personal-playlist',
        7: 'promotion',
        8: 'chart-item',
        9: 'play-context',
        10: 'mix-link',
        11: 'personal-playlists',
        12: 'play-contexts',
        13: 'user',
        14: 'podcast',
        15: 'podcast_episode',
    }


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5, 13, 14, 15])
def result_with_type(
    request: pytest.FixtureRequest,
    results: Dict[int, ResultItem],
    types: Dict[int, str],
) -> Tuple[SearchItem, str]:
    return as_search_item(results[request.param]), types[request.param]


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5, 13, 14, 15])
def best(
    request: pytest.FixtureRequest,
    results: Dict[int, ResultItem],
    types: Dict[int, str],
) -> Best:
    return Best(types[request.param], as_search_item(results[request.param]), TestBest.text)


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5, 13, 14, 15])
def best_with_result(
    request: pytest.FixtureRequest,
    results: Dict[int, ResultItem],
    types: Dict[int, str],
) -> Tuple[Best, SearchItem]:
    result = as_search_item(results[request.param])
    return Best(types[request.param], result, TestBest.text), result


@pytest.fixture(scope='session', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity(
    request: pytest.FixtureRequest,
    results: Dict[int, ResultItem],
    types: Dict[int, str],
) -> BlockEntity:
    return BlockEntity(TestBlockEntity.id, types[request.param], as_block_entity_data(results[request.param]))


@pytest.fixture(scope='session')
def block(block_entity: BlockEntity, data_with_type: Tuple[BlockData, str]) -> Block:
    data, type_ = data_with_type

    return Block(
        TestBlock.id, type_, TestBlock.type_for_from, TestBlock.title, [block_entity], TestBlock.description, data
    )


@pytest.fixture(scope='session', params=[11, 12])
def data(
    request: pytest.FixtureRequest,
    results: Dict[int, ResultItem],
) -> BlockData:
    return as_block_data(results[request.param])


@pytest.fixture(scope='session', params=[11, 12])
def data_with_type(
    request: pytest.FixtureRequest,
    results: Dict[int, ResultItem],
    types: Dict[int, str],
) -> Tuple[BlockData, str]:
    return as_block_data(results[request.param]), types[request.param]


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5])
def search_result_with_results_and_type(
    request: pytest.FixtureRequest,
    types: Dict[int, str],
    results: Dict[int, ResultItem],
) -> Tuple[
    SearchResult[SearchItem],
    List[SearchItem],
    str,
]:
    result = as_search_item(results[request.param])
    return (
        SearchResult(
            types[request.param],
            TestSearchResult.total,
            TestSearchResult.per_page,
            TestSearchResult.order,
            [result],
        ),
        [result],
        types[request.param],
    )


@pytest.fixture(scope='session')
def custom_wave() -> CustomWave:
    return CustomWave(TestCustomWave.title, TestCustomWave.animation_url, TestCustomWave.position)


@pytest.fixture(scope='session')
def r_128() -> R128:
    return R128(TestR128.i, TestR128.tp, TestR128.important_secs)


@pytest.fixture(scope='session')
def lyrics_info() -> LyricsInfo:
    return LyricsInfo(TestLyricsInfo.has_available_sync_lyrics, TestLyricsInfo.has_available_text_lyrics)


@pytest.fixture(scope='session')
def stats() -> Stats:
    return Stats(TestStats.last_month_listeners, TestStats.last_month_listeners_delta)


@pytest.fixture(scope='session')
def pin_data_artist(cover: Cover, content_restrictions: ContentRestrictions) -> PinData:
    return PinData(
        id=TestPinData.id,
        name=TestPinData.name,
        cover=cover,
        content_restrictions=content_restrictions,
    )


@pytest.fixture(scope='session')
def pin_data_album(cover: Cover, content_restrictions: ContentRestrictions) -> PinData:
    return PinData(
        id=TestPinData.id,
        title=TestPinData.title,
        cover=cover,
        content_restrictions=content_restrictions,
    )


@pytest.fixture(scope='session')
def pin_data_playlist(cover: Cover) -> PinData:
    return PinData(
        uid=TestPinData.uid,
        kind=TestPinData.kind,
        playlist_uuid=TestPinData.playlist_uuid,
        title=TestPinData.title,
        cover=cover,
    )


@pytest.fixture(scope='session')
def pin_artist(pin_data_artist: PinData) -> Pin:
    return Pin(type=TestPin.type_artist, data=pin_data_artist)


@pytest.fixture(scope='session')
def pin_album(pin_data_album: PinData) -> Pin:
    return Pin(type=TestPin.type_album, data=pin_data_album)


@pytest.fixture(scope='session')
def pin_playlist(pin_data_playlist: PinData) -> Pin:
    return Pin(type=TestPin.type_playlist, data=pin_data_playlist)


@pytest.fixture(scope='session')
def pins_list(pin_artist: Pin) -> PinsList:
    return PinsList(
        pins=[pin_artist],
    )


@pytest.fixture(scope='session')
def presaves(album: Album) -> Presaves:
    return Presaves(
        upcoming_albums=[album],
        released_albums=[album],
    )


@pytest.fixture(scope='session')
def wave() -> Wave:
    return Wave(
        name=TestWave.name,
        description=TestWave.description,
        seeds=TestWave.seeds,
        station_id=TestWave.station_id,
        id_for_from=TestWave.id_for_from,
        type=TestWave.type,
    )


@pytest.fixture(scope='session')
def wave_agent_entity() -> WaveAgentEntity:
    return WaveAgentEntity(type=TestWaveAgentEntity.type)


@pytest.fixture(scope='session')
def wave_agent(cover: Cover, wave_agent_entity: WaveAgentEntity) -> WaveAgent:
    return WaveAgent(
        animation_uri=TestWaveAgent.animation_uri,
        cover=cover,
        entity=wave_agent_entity,
    )


@pytest.fixture(scope='session')
def similar_entity_data(wave: Wave, wave_agent: WaveAgent) -> SimilarEntityData:
    return SimilarEntityData(wave=wave, agent=wave_agent)


@pytest.fixture(scope='session')
def similar_entity_item(similar_entity_data: SimilarEntityData) -> SimilarEntityItem:
    return SimilarEntityItem(
        type=TestSimilarEntityItem.type,
        data=similar_entity_data,
    )


@pytest.fixture(scope='session')
def album_similar_entities(similar_entity_item: SimilarEntityItem) -> AlbumSimilarEntities:
    return AlbumSimilarEntities(
        items=[similar_entity_item],
    )


@pytest.fixture(scope='session')
def trailer_info(track: Track) -> TrailerInfo:
    return TrailerInfo(
        title=TestTrailerInfo.title,
        tracks=[track],
    )


@pytest.fixture(scope='session')
def album_trailer(album: Album, artist: Artist, trailer_info: TrailerInfo) -> AlbumTrailer:
    return AlbumTrailer(
        album=album,
        artists=[artist],
        trailer=trailer_info,
    )


@pytest.fixture(scope='session')
def foreign_agent() -> ForeignAgent:
    return ForeignAgent(
        reason=TestForeignAgent.reason,
        title=TestForeignAgent.title,
    )


@pytest.fixture(scope='session')
def disclaimer(foreign_agent: ForeignAgent) -> Disclaimer:
    return Disclaimer(
        foreign_agent=foreign_agent,
    )


@pytest.fixture(scope='session')
def experiment_detail_value() -> ExperimentDetailValue:
    value = ExperimentDetailValue(title=TestExperimentDetailValue.title)
    value.__dict__['enabled'] = TestExperimentDetailValue.enabled
    value.__dict__['delay'] = TestExperimentDetailValue.delay
    return value


@pytest.fixture(scope='session')
def experiment_detail(experiment_detail_value: ExperimentDetailValue) -> ExperimentDetail:
    return ExperimentDetail(group=TestExperimentDetail.group, value=experiment_detail_value)


@pytest.fixture(scope='session')
def experiments_details(experiment_detail: ExperimentDetail) -> ExperimentsDetails:
    return ExperimentsDetails(experiments={'TestExperiment': experiment_detail})


@pytest.fixture(scope='session')
def fade() -> Fade:
    return Fade(
        in_start=TestFade.in_start,
        in_stop=TestFade.in_stop,
        out_start=TestFade.out_start,
        out_stop=TestFade.out_stop,
    )


@pytest.fixture(scope='session')
def smart_preview_params(fade: Fade) -> SmartPreviewParams:
    return SmartPreviewParams(
        duration_ms=TestSmartPreviewParams.duration_ms,
        fade=fade,
    )


@pytest.fixture(scope='session')
def credit() -> Credit:
    return Credit(
        title=TestCredit.title,
        value=TestCredit.value,
    )


@pytest.fixture(scope='session')
def credits_(credit: Credit) -> Credits:
    return Credits(
        credits=[credit],
    )


@pytest.fixture(scope='session')
def file_download_info() -> FileDownloadInfo:
    return FileDownloadInfo(
        track_id=TestFileDownloadInfo.track_id,
        quality=TestFileDownloadInfo.quality,
        codec=TestFileDownloadInfo.codec,
        bitrate=TestFileDownloadInfo.bitrate,
        transport=TestFileDownloadInfo.transport,
        url=TestFileDownloadInfo.url,
        urls=TestFileDownloadInfo.urls,
        real_id=TestFileDownloadInfo.real_id,
        gain=TestFileDownloadInfo.gain,
        key=TestFileDownloadInfo.key,
    )


@pytest.fixture(scope='session')
def file_info(file_download_info: FileDownloadInfo) -> FileInfo:
    return FileInfo(download_info=file_download_info)


@pytest.fixture(scope='session')
def track_trailer(track: Track) -> TrackTrailer:
    return TrackTrailer(
        title=TestTrackTrailer.title,
        track=track,
    )


@pytest.fixture(scope='session')
def track_full_info(track: Track, artist: Artist) -> TrackFullInfo:
    return TrackFullInfo(
        track=track,
        similar_tracks=[track],
        also_in_albums=[track],
        aliases=TestTrackFullInfo.aliases,
        artists=[artist],
    )


@pytest.fixture(scope='session')
def artist_link() -> ArtistLink:
    return ArtistLink(TestArtistLink.title, TestArtistLink.subtitle, TestArtistLink.url, TestArtistLink.img_url)


@pytest.fixture(scope='session')
def artist_links_fixture(artist_link: ArtistLink) -> ArtistLinks:
    return ArtistLinks(
        links=[artist_link],
    )


@pytest.fixture(scope='session')
def artist_similar(artist: Artist) -> ArtistSimilar:
    return ArtistSimilar(
        artist=artist,
        similar_artists=[artist],
    )


@pytest.fixture(scope='session')
def music_history_item_id() -> MusicHistoryItemId:
    return MusicHistoryItemId(
        id=TestMusicHistoryItemId.id,
        track_id=TestMusicHistoryItemId.track_id,
        album_id=TestMusicHistoryItemId.album_id,
    )


@pytest.fixture(scope='session')
def music_history_context_full_model_album(album_without_tracks: Album, artist: Artist) -> MusicHistoryContextFullModel:
    return MusicHistoryContextFullModel(
        album=album_without_tracks,
        artists=[artist],
        available=TestMusicHistoryContextFullModel.available,
    )


@pytest.fixture(scope='session')
def music_history_context_full_model_artist(artist: Artist) -> MusicHistoryContextFullModel:
    return MusicHistoryContextFullModel(
        artist=artist,
        available=TestMusicHistoryContextFullModel.available,
    )


@pytest.fixture(scope='session')
def music_history_item_data_track(music_history_item_id: MusicHistoryItemId, track: Track) -> MusicHistoryItemData:
    return MusicHistoryItemData(
        item_id=music_history_item_id,
        full_model=track,
    )


@pytest.fixture(scope='session')
def music_history_item_data_context(
    music_history_item_id: MusicHistoryItemId, music_history_context_full_model_album: MusicHistoryContextFullModel
) -> MusicHistoryItemData:
    return MusicHistoryItemData(
        item_id=music_history_item_id,
        full_model=music_history_context_full_model_album,
    )


@pytest.fixture(scope='session')
def music_history_item_track(music_history_item_data_track: MusicHistoryItemData) -> MusicHistoryItem:
    return MusicHistoryItem(
        type=TestMusicHistoryItem.type_track,
        data=music_history_item_data_track,
    )


@pytest.fixture(scope='session')
def music_history_item_album(music_history_item_data_context: MusicHistoryItemData) -> MusicHistoryItem:
    return MusicHistoryItem(
        type=TestMusicHistoryItem.type_album,
        data=music_history_item_data_context,
    )


@pytest.fixture(scope='session')
def music_history_group(
    music_history_item_album: MusicHistoryItem, music_history_item_track: MusicHistoryItem
) -> MusicHistoryGroup:
    return MusicHistoryGroup(
        context=music_history_item_album,
        tracks=[music_history_item_track],
    )


@pytest.fixture(scope='session')
def music_history_tab(music_history_group: MusicHistoryGroup) -> MusicHistoryTab:
    return MusicHistoryTab(
        date=TestMusicHistoryTab.date,
        items=[music_history_group],
    )


@pytest.fixture(scope='session')
def music_history(music_history_tab: MusicHistoryTab) -> MusicHistory:
    return MusicHistory(
        history_tabs=[music_history_tab],
    )


@pytest.fixture(scope='session')
def music_history_items(music_history_item_track: MusicHistoryItem) -> MusicHistoryItems:
    return MusicHistoryItems(
        items=[music_history_item_track],
    )


@pytest.fixture(scope='session')
def artist_trailer_status() -> ArtistTrailerStatus:
    return ArtistTrailerStatus(
        available=TestArtistTrailerStatus.available,
    )


@pytest.fixture(scope='session')
def about_artist(artist: Artist, stats: Stats, artist_link: ArtistLink, cover: Cover) -> ArtistAbout:
    return ArtistAbout(
        artist=artist,
        stats=stats,
        description=TestArtistAbout.description,
        links=[artist_link],
        covers=[cover],
        artist_type=TestArtistAbout.artist_type,
    )


@pytest.fixture(scope='session')
def artist_clip_data(clip: Clip, artist: Artist) -> ArtistClipData:
    return ArtistClipData(
        clip=clip,
        artists=[artist],
    )


@pytest.fixture(scope='session')
def artist_clip_item(artist_clip_data: ArtistClipData) -> ArtistClipItem:
    return ArtistClipItem(
        type=TestArtistClipItem.type,
        data=artist_clip_data,
    )


@pytest.fixture(scope='session')
def artist_clips(artist_clip_item: ArtistClipItem, pager: Pager) -> ArtistClips:
    return ArtistClips(
        items=[artist_clip_item],
        pager=pager,
    )


@pytest.fixture(scope='session')
def artist_info(artist: Artist, stats: Stats, artist_trailer_status: ArtistTrailerStatus, cover: Cover) -> ArtistInfo:
    return ArtistInfo(
        artist=artist,
        likes_count=TestArtistInfo.likes_count,
        stats=stats,
        trailer=artist_trailer_status,
        covers=[cover],
        description=TestArtistInfo.description,
        artist_type=TestArtistInfo.artist_type,
    )


@pytest.fixture(scope='session')
def artist_trailer(artist: Artist, trailer_info: TrailerInfo) -> ArtistTrailer:
    return ArtistTrailer(
        artist=artist,
        trailer=trailer_info,
    )


@pytest.fixture(scope='session')
def skeleton_source() -> SkeletonSource:
    return SkeletonSource(
        uri=TestSkeletonSource.uri,
        count_web=TestSkeletonSource.count_web,
        count=TestSkeletonSource.count,
    )


@pytest.fixture(scope='session')
def skeleton_view_all_action() -> SkeletonViewAllAction:
    return SkeletonViewAllAction(
        deeplink=TestSkeletonViewAllAction.deeplink,
        weblink=TestSkeletonViewAllAction.weblink,
    )


@pytest.fixture(scope='session')
def skeleton_block_data(
    skeleton_source: SkeletonSource, skeleton_view_all_action: SkeletonViewAllAction
) -> SkeletonBlockData:
    return SkeletonBlockData(
        source=skeleton_source,
        title=TestSkeletonBlockData.title,
        show_policy=TestSkeletonBlockData.show_policy,
        view_all_action=skeleton_view_all_action,
    )


@pytest.fixture(scope='session')
def skeleton_block(skeleton_block_data: SkeletonBlockData) -> SkeletonBlock:
    return SkeletonBlock(
        id=TestSkeletonBlock.id,
        type=TestSkeletonBlock.type,
        data=skeleton_block_data,
    )


@pytest.fixture(scope='session')
def skeleton_tab(skeleton_block: SkeletonBlock) -> SkeletonTab:
    return SkeletonTab(
        id=TestSkeletonTab.id,
        title=TestSkeletonTab.title,
        blocks=[skeleton_block],
    )


@pytest.fixture(scope='session')
def artist_skeleton(skeleton_block: SkeletonBlock) -> ArtistSkeleton:
    return ArtistSkeleton(
        id=TestArtistSkeleton.id,
        title=TestArtistSkeleton.title,
        blocks=[skeleton_block],
    )


@pytest.fixture(scope='session')
def artist_donation_goal() -> ArtistDonationGoal:
    return ArtistDonationGoal(
        title=TestArtistDonationGoal.title,
    )


@pytest.fixture(scope='session')
def artist_donation_data(artist: Artist, artist_donation_goal: ArtistDonationGoal) -> ArtistDonationData:
    return ArtistDonationData(
        tip_url=TestArtistDonationData.tip_url,
        artist=artist,
        goal=artist_donation_goal,
    )


@pytest.fixture(scope='session')
def artist_donation_item(artist_donation_data: ArtistDonationData) -> ArtistDonationItem:
    return ArtistDonationItem(
        type=TestArtistDonationItem.type,
        data=artist_donation_data,
    )


@pytest.fixture(scope='session')
def artist_donations(artist_donation_item: ArtistDonationItem) -> ArtistDonations:
    return ArtistDonations(
        donations=[artist_donation_item],
    )


@pytest.fixture(scope='session')
def playlist_availability() -> PlaylistAvailability:
    return PlaylistAvailability(
        available=TestPlaylistAvailability.available,
    )


@pytest.fixture(scope='session')
def playlist_trailer(playlist: Playlist, trailer_info: TrailerInfo) -> PlaylistTrailer:
    return PlaylistTrailer(
        playlist=playlist,
        trailer=trailer_info,
        shareable=TestPlaylistTrailer.shareable,
    )


@pytest.fixture(scope='session')
def playlist_similar_entities(similar_entity_item: SimilarEntityItem) -> PlaylistSimilarEntities:
    return PlaylistSimilarEntities(
        items=[similar_entity_item],
    )


@pytest.fixture(scope='session')
def playlists_list(playlist: Playlist) -> PlaylistsList:
    return PlaylistsList(
        playlists=[playlist],
    )


@pytest.fixture(scope='session')
def metatag_title() -> MetatagTitle:
    return MetatagTitle(title=TestMetatagTitle.title, full_title=TestMetatagTitle.full_title)


@pytest.fixture(scope='session')
def metatag_sort_by_value() -> MetatagSortByValue:
    return MetatagSortByValue(
        value=TestMetatagSortByValue.value,
        title=TestMetatagSortByValue.title,
        active=TestMetatagSortByValue.active,
    )


@pytest.fixture(scope='session')
def metatag_leaf_nested() -> MetatagLeaf:
    return MetatagLeaf(tag='Спокойная музыка', title='Спокойное')


@pytest.fixture(scope='session')
def metatag_leaf(metatag_leaf_nested: MetatagLeaf) -> MetatagLeaf:
    return MetatagLeaf(
        tag=TestMetatagLeaf.tag,
        title=TestMetatagLeaf.title,
        leaves=[metatag_leaf_nested],
    )


@pytest.fixture(scope='session')
def metatag_tree(metatag_leaf: MetatagLeaf) -> MetatagTree:
    return MetatagTree(
        title=TestMetatagTree.title,
        navigation_id=TestMetatagTree.navigation_id,
        leaves=[metatag_leaf],
    )


@pytest.fixture(scope='session')
def metatags(metatag_tree: MetatagTree) -> Metatags:
    return Metatags(trees=[metatag_tree])


@pytest.fixture(scope='session')
def metatag(
    metatag_title: MetatagTitle,
    artist: Artist,
    album: Album,
    playlist: Playlist,
    metatag_sort_by_value: MetatagSortByValue,
) -> Metatag:
    return Metatag(
        id=TestMetatag.id,
        cover_uri=TestMetatag.cover_uri,
        color=TestMetatag.color,
        title=metatag_title,
        liked=TestMetatag.liked,
        station_id=TestMetatag.station_id,
        custom_wave_animation_url=TestMetatag.custom_wave_animation_url,
        artists=[artist],
        albums=[album],
        playlists=[playlist],
        tracks_sort_by_values=[metatag_sort_by_value],
        albums_sort_by_values=[metatag_sort_by_value],
        playlists_sort_by_values=[metatag_sort_by_value],
    )


@pytest.fixture(scope='session')
def metatag_artist_entry(artist: Artist, track: Track) -> MetatagArtistEntry:
    return MetatagArtistEntry(artist=artist, popular_tracks=[track])


@pytest.fixture(scope='session')
def metatag_artists(
    metatag_title: MetatagTitle,
    metatag_artist_entry: MetatagArtistEntry,
    pager: Pager,
    metatag_sort_by_value: MetatagSortByValue,
) -> MetatagArtists:
    return MetatagArtists(
        id=TestMetatagArtists.id,
        cover_uri=TestMetatagArtists.cover_uri,
        color=TestMetatagArtists.color,
        title=metatag_title,
        station_id=TestMetatagArtists.station_id,
        pager=pager,
        artists=[metatag_artist_entry],
        sort_by_values=[metatag_sort_by_value],
    )


@pytest.fixture(scope='session')
def metatag_albums(
    metatag_title: MetatagTitle, album: Album, pager: Pager, metatag_sort_by_value: MetatagSortByValue
) -> MetatagAlbums:
    return MetatagAlbums(
        id=TestMetatagAlbums.id,
        cover_uri=TestMetatagAlbums.cover_uri,
        color=TestMetatagAlbums.color,
        title=metatag_title,
        station_id=TestMetatagAlbums.station_id,
        pager=pager,
        albums=[album],
        sort_by_values=[metatag_sort_by_value],
    )


@pytest.fixture(scope='session')
def metatag_playlists(
    metatag_title: MetatagTitle, playlist: Playlist, pager: Pager, metatag_sort_by_value: MetatagSortByValue
) -> MetatagPlaylists:
    return MetatagPlaylists(
        id=TestMetatagPlaylists.id,
        cover_uri=TestMetatagPlaylists.cover_uri,
        color=TestMetatagPlaylists.color,
        title=metatag_title,
        station_id=TestMetatagPlaylists.station_id,
        pager=pager,
        playlists=[playlist],
        sort_by_values=[metatag_sort_by_value],
    )


@pytest.fixture(scope='session')
def rotor_seed() -> RotorSeed:
    return RotorSeed(TestRotorSeed.type, TestRotorSeed.tag, TestRotorSeed.value)


@pytest.fixture(scope='session')
def track_parameters(fade: Fade) -> TrackParameters:
    return TrackParameters(
        TestTrackParameters.bpm,
        TestTrackParameters.energy,
        TestTrackParameters.hue,
        TestTrackParameters.user_collection_hue,
        fade,
    )


@pytest.fixture(scope='session')
def rotor_session(sequence: Sequence, rotor_seed: RotorSeed, wave: Wave) -> RotorSession:
    return RotorSession(
        TestRotorSession.radio_session_id,
        TestRotorSession.batch_id,
        TestRotorSession.pumpkin,
        [sequence],
        [rotor_seed],
        rotor_seed,
        TestRotorSession.terminated,
        wave,
        TestRotorSession.offline_recommender_data,
        TestRotorSession.interactive,
    )


@pytest.fixture(scope='session')
def rotor_session_tracks(sequence: Sequence) -> RotorSessionTracks:
    return RotorSessionTracks(
        TestRotorSessionTracks.batch_id,
        TestRotorSessionTracks.pumpkin,
        [sequence],
        TestRotorSessionTracks.terminated,
        TestRotorSessionTracks.unknown_session,
        TestRotorSessionTracks.offline_recommender_data,
    )


@pytest.fixture(scope='session')
def session_playable() -> SessionPlayable:
    return SessionPlayable(TestSessionPlayable.type, TestSessionPlayable.track_id, TestSessionPlayable.id)


@pytest.fixture(scope='session')
def session_event(session_playable: SessionPlayable) -> SessionEvent:
    return SessionEvent(
        TestSessionEvent.type,
        TestSessionEvent.timestamp,
        TestSessionEvent.track_id,
        TestSessionEvent.total_played_seconds,
        session_playable,
    )


@pytest.fixture(scope='session')
def session_feedback(session_event: SessionEvent) -> SessionFeedback:
    return SessionFeedback(session_event, TestSessionFeedback.batch_id, TestSessionFeedback.from_)


@pytest.fixture(scope='session')
def session_feedbacks(session_feedback: SessionFeedback) -> SessionFeedbacks:
    return SessionFeedbacks(TestSessionFeedbacks.session_id, [session_feedback])


@pytest.fixture(scope='session')
def combined_session_item(clip: Clip) -> CombinedSessionItem:
    return CombinedSessionItem(TestCombinedSessionItem.type, clip)


@pytest.fixture(scope='session')
def combined_session(combined_session_item: CombinedSessionItem) -> CombinedSession:
    return CombinedSession(
        TestCombinedSession.session_id,
        TestCombinedSession.batch_id,
        TestCombinedSession.pumpkin,
        [combined_session_item],
    )


@pytest.fixture(scope='session')
def combined_session_landing(combined_session_item: CombinedSessionItem) -> CombinedSessionLanding:
    return CombinedSessionLanding(
        TestCombinedSessionLanding.title,
        TestCombinedSessionLanding.description,
        TestCombinedSessionLanding.button,
        [combined_session_item],
    )


@pytest.fixture(scope='session')
def combined_session_queue_item() -> CombinedSessionQueueItem:
    return CombinedSessionQueueItem(TestCombinedSessionQueueItem.type, TestCombinedSessionQueueItem.id)


@pytest.fixture(scope='session')
def generative_stream_info() -> GenerativeStreamInfo:
    return GenerativeStreamInfo(TestGenerativeStreamInfo.id, TestGenerativeStreamInfo.url)


@pytest.fixture(scope='session')
def generative_stream_data(cover_derived_colors: CoverDerivedColors) -> GenerativeStreamData:
    return GenerativeStreamData(
        TestGenerativeStreamData.title,
        TestGenerativeStreamData.subtitle,
        TestGenerativeStreamData.background_color,
        cover_derived_colors,
        TestGenerativeStreamData.image_url,
        TestGenerativeStreamData.video_cover_uri,
        TestGenerativeStreamData.explanations,
    )


@pytest.fixture(scope='session')
def generative_stream(
    generative_stream_data: GenerativeStreamData, generative_stream_info: GenerativeStreamInfo
) -> GenerativeStream:
    return GenerativeStream(generative_stream_data, TestGenerativeStream.version, generative_stream_info)


@pytest.fixture(scope='session')
def generative_stream_feedback() -> GenerativeStreamFeedback:
    return GenerativeStreamFeedback(TestGenerativeStreamFeedback.reload_stream, TestGenerativeStreamFeedback.not_paused)


@pytest.fixture(scope='session')
def wave_default_station() -> WaveDefaultStation:
    return WaveDefaultStation(
        TestWaveDefaultStation.station_id,
        TestWaveDefaultStation.title,
        TestWaveDefaultStation.rup_title,
        TestWaveDefaultStation.rup_description,
    )


@pytest.fixture(scope='session')
def wave_settings_block(station: Station) -> WaveSettingsBlock:
    return WaveSettingsBlock(TestWaveSettingsBlock.type, [station])


@pytest.fixture(scope='session')
def wave_settings(
    wave_default_station: WaveDefaultStation, wave_settings_block: WaveSettingsBlock, restrictions: Restrictions
) -> WaveSettings:
    return WaveSettings(wave_default_station, [wave_settings_block], restrictions)
