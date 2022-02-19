import pytest

from yandex_music import (
    Account,
    AdParams,
    Album,
    AlbumEvent,
    Artist,
    ArtistEvent,
    AutoRenewable,
    Best,
    Block,
    BlockEntity,
    CaseForms,
    Chart,
    ChartInfo,
    ChartInfoMenu,
    ChartInfoMenuItem,
    ChartItem,
    Client,
    Counts,
    Cover,
    Day,
    Description,
    DiscreteScale,
    Enum,
    Event,
    GeneratedPlaylist,
    Icon,
    Id,
    Images,
    InvocationInfo,
    Label,
    LicenceTextPart,
    Link,
    Lyrics,
    MadeFor,
    Major,
    MetaData,
    MixLink,
    Normalization,
    Pager,
    PassportPhone,
    Permissions,
    PersonalPlaylistsData,
    PlayContext,
    PlayContextsData,
    PlayCounter,
    Playlist,
    PlaylistAbsence,
    PlaylistId,
    Plus,
    Price,
    Product,
    Promotion,
    Ratings,
    RenewableRemainder,
    Restrictions,
    RotorSettings,
    SearchResult,
    Sequence,
    Settings,
    Shot,
    ShotData,
    ShotType,
    Station,
    StationResult,
    Status,
    Subscription,
    Tag,
    Title,
    Track,
    TrackId,
    TrackPosition,
    TrackShort,
    TrackShortOld,
    TrackWithAds,
    User,
    Value,
    Video,
    VideoSupplement,
    Vinyl,
    StationData,
    AlertButton,
    Alert,
    NonAutoRenewable,
    PoetryLoverMatch,
    Deactivation,
    Operator,
    Contest,
    OpenGraphData,
    Brand,
    Context,
    Deprecation,
)
from . import (
    TestAccount,
    TestAdParams,
    TestAlbum,
    TestArtist,
    TestAutoRenewable,
    TestBest,
    TestBlock,
    TestBlockEntity,
    TestCaseForms,
    TestChart,
    TestChartInfo,
    TestChartInfoMenuItem,
    TestCounts,
    TestCover,
    TestDay,
    TestDescription,
    TestDiscreteScale,
    TestEnum,
    TestEvent,
    TestGeneratedPlaylist,
    TestIcon,
    TestId,
    TestImages,
    TestInvocationInfo,
    TestLabel,
    TestLicenceTextPart,
    TestLink,
    TestLyrics,
    TestMajor,
    TestMetaData,
    TestMixLink,
    TestNormalization,
    TestPager,
    TestPassportPhone,
    TestPermissions,
    TestPersonalPlaylistsData,
    TestPlayContext,
    TestPlayCounter,
    TestPlaylist,
    TestPlaylistAbsence,
    TestPlaylistId,
    TestPlus,
    TestPrice,
    TestProduct,
    TestPromotion,
    TestRatings,
    TestRenewableRemainder,
    TestRotorSettings,
    TestSearchResult,
    TestSequence,
    TestSettings,
    TestShot,
    TestShotData,
    TestShotType,
    TestStation,
    TestStationResult,
    TestStatus,
    TestSubscription,
    TestTag,
    TestTitle,
    TestTrack,
    TestTrackId,
    TestTrackPosition,
    TestTrackShort,
    TestTrackShortOld,
    TestTrackWithAds,
    TestUser,
    TestValue,
    TestVideo,
    TestVideoSupplement,
    TestVinyl,
    TestArtistEvent,
    TestStationData,
    TestAlertButton,
    TestAlert,
    TestNonAutoRenewable,
    TestPoetryLoverMatch,
    TestDeactivation,
    TestOperator,
    TestContest,
    TestOpenGraphData,
    TestBrand,
    TestContext,
    TestDeprecation,
)


@pytest.fixture(scope='session')
def artist_factory(cover, counts, ratings, link, description):
    class ArtistFactory:
        def get(self, popular_tracks, decomposed=None):
            return Artist(
                TestArtist.id,
                TestArtist.error,
                TestArtist.reason,
                TestArtist.name,
                cover,
                TestArtist.various,
                TestArtist.composer,
                TestArtist.genres,
                TestArtist.og_image,
                TestArtist.op_image,
                TestArtist.no_pictures_from_search,
                counts,
                TestArtist.available,
                ratings,
                [link],
                TestArtist.tickets_available,
                TestArtist.likes_count,
                popular_tracks,
                TestArtist.regions,
                decomposed,
                TestArtist.full_names,
                TestArtist.hand_made_description,
                description,
                TestArtist.countries,
                TestArtist.en_wikipedia_link,
                TestArtist.db_aliases,
                TestArtist.aliases,
                TestArtist.init_date,
                TestArtist.end_date,
                TestArtist.ya_money_id,
            )

    return ArtistFactory()


@pytest.fixture(scope='session')
def artist(artist_factory, track_without_artists_and_albums, artist_decomposed):
    return artist_factory.get([track_without_artists_and_albums], artist_decomposed)


@pytest.fixture(scope='session')
def artist_without_nested_artist(artist_factory, track_without_artists_and_albums):
    return artist_factory.get([track_without_artists_and_albums])


@pytest.fixture(scope='session')
def artist_without_tracks(artist_factory):
    return artist_factory.get([])


@pytest.fixture(scope='session')
def artist_decomposed(artist_without_nested_artist):
    return [' & ', artist_without_nested_artist]


@pytest.fixture(scope='session')
def track_factory(major, normalization, user, meta_data, poetry_lover_match):
    class TrackFactory:
        def get(self, artists, albums, track_without_nested_tracks=None):
            return Track(
                TestTrack.id,
                TestTrack.title,
                TestTrack.available,
                artists,
                albums,
                TestTrack.available_for_premium_users,
                TestTrack.lyrics_available,
                [poetry_lover_match],
                TestTrack.best,
                TestTrack.real_id,
                TestTrack.og_image,
                TestTrack.type,
                TestTrack.cover_uri,
                major,
                TestTrack.duration_ms,
                TestTrack.storage_dir,
                TestTrack.file_size,
                track_without_nested_tracks,
                track_without_nested_tracks,
                normalization,
                TestTrack.error,
                TestTrack.can_publish,
                TestTrack.state,
                TestTrack.desired_visibility,
                TestTrack.filename,
                user,
                meta_data,
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
            )

    return TrackFactory()


@pytest.fixture(scope='session')
def track(track_factory, artist, album, track_without_nested_tracks):
    return track_factory.get([artist], [album], track_without_nested_tracks)


@pytest.fixture(scope='session')
def track_without_artists(track_factory, album):
    return track_factory.get([], [album])


@pytest.fixture(scope='session')
def track_without_albums(track_factory, artist):
    return track_factory.get([artist], [])


@pytest.fixture(scope='session')
def track_without_artists_and_albums(track_factory):
    return track_factory.get([], [])


@pytest.fixture(scope='session')
def track_without_nested_tracks(artist, album, track_factory):
    return track_factory.get([artist], [album])


@pytest.fixture(scope='session')
def album_factory(label, track_position):
    class AlbumFactory:
        def get(self, artists, volumes, albums=None, deprecation=None):
            return Album(
                TestAlbum.id,
                TestAlbum.error,
                TestAlbum.title,
                TestAlbum.track_count,
                artists,
                [label],
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
                albums,
                TestAlbum.prerolls,
                volumes,
                TestAlbum.year,
                TestAlbum.release_date,
                TestAlbum.type,
                track_position,
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
            )

    return AlbumFactory()


@pytest.fixture(scope='session')
def album(album_factory, artist_without_tracks, track_without_albums, album_without_nested_albums, deprecation):
    return album_factory.get(
        [artist_without_tracks], [[track_without_albums]], [album_without_nested_albums], deprecation
    )


@pytest.fixture(scope='session')
def album_without_tracks(album_factory, artist_without_tracks):
    return album_factory.get([artist_without_tracks], [])


@pytest.fixture(scope='session')
def album_without_nested_albums(album_factory, artist_without_tracks, track_without_albums):
    return album_factory.get([artist_without_tracks], [[track_without_albums]])


@pytest.fixture(scope='session')
def playlist_factory(
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
):
    class PlaylistFactory:
        def get(self, similar_playlists, last_owner_playlists):
            return Playlist(
                user,
                cover,
                made_for,
                play_counter,
                playlist_absence,
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
                cover,
                contest,
                TestPlaylist.background_color,
                TestPlaylist.text_color,
                TestPlaylist.id_for_from,
                TestPlaylist.dummy_description,
                TestPlaylist.dummy_page_description,
                cover,
                cover,
                open_graph_data,
                brand,
                TestPlaylist.metrika_id,
                TestPlaylist.coauthors,
                [artist],
                [track_id],
                [track_short],
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
            )

    return PlaylistFactory()


@pytest.fixture(scope='session')
def playlist(playlist_factory, playlist_without_nested_playlists):
    return playlist_factory.get([playlist_without_nested_playlists], [playlist_without_nested_playlists])


@pytest.fixture(scope='session')
def playlist_without_nested_playlists(playlist_factory):
    return playlist_factory.get([], [])


@pytest.fixture(scope='session')
def generated_playlist(playlist):
    return GeneratedPlaylist(
        TestGeneratedPlaylist.type,
        TestGeneratedPlaylist.ready,
        TestGeneratedPlaylist.notify,
        playlist,
        TestGeneratedPlaylist.description,
    )


@pytest.fixture(scope='session')
def client():
    return Client()


@pytest.fixture(scope='session')
def tag():
    return Tag(TestTag.id_, TestTag.value, TestTag.name, TestTag.og_description, TestTag.og_image)


@pytest.fixture(scope='session')
def brand():
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
def track_with_ads(track):
    return TrackWithAds(TestTrackWithAds.type, track)


@pytest.fixture(scope='session')
def day(event, track_with_ads, track):
    return Day(TestDay.day, [event], [track_with_ads], [track])


@pytest.fixture(scope='session')
def track_short():
    return TrackShort(TestTrackShort.id, TestTrackShort.timestamp, TestTrackShort.album_id)


@pytest.fixture(scope='session')
def track_short_old(track_id):
    return TrackShortOld(track_id, TestTrackShortOld.timestamp)


@pytest.fixture(scope='session')
def video():
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
def vinyl():
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
def play_context(track_short_old):
    return PlayContext(
        TestPlayContext.client_, TestPlayContext.context, TestPlayContext.context_item, [track_short_old]
    )


@pytest.fixture(scope='session')
def play_contexts_data(track_short_old):
    return PlayContextsData([track_short_old])


@pytest.fixture(scope='session')
def enum(value):
    return Enum(TestEnum.type, TestEnum.name, [value])


@pytest.fixture(scope='session')
def icon():
    return Icon(TestIcon.background_color, TestIcon.image_url)


@pytest.fixture(scope='session')
def cover():
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
    )


@pytest.fixture(scope='session')
def open_graph_data(cover):
    return OpenGraphData(TestOpenGraphData.title, TestOpenGraphData.description, cover)


@pytest.fixture(scope='session')
def meta_data():
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
def licence_text_part():
    return LicenceTextPart(TestLicenceTextPart.text, TestLicenceTextPart.url)


@pytest.fixture(scope='session')
def link():
    return Link(TestLink.title, TestLink.href, TestLink.type, TestLink.social_network)


@pytest.fixture(scope='session')
def invocation_info():
    return InvocationInfo(
        TestInvocationInfo.hostname, TestInvocationInfo.req_id, TestInvocationInfo.exec_duration_millis
    )


@pytest.fixture(scope='session')
def settings(product, price):
    return Settings([product], [product], TestSettings.web_payment_url, TestSettings.promo_codes_enabled, price)


@pytest.fixture(scope='session')
def counts():
    return Counts(TestCounts.tracks, TestCounts.direct_albums, TestCounts.also_albums, TestCounts.also_tracks)


@pytest.fixture(scope='session')
def description():
    return Description(TestDescription.text, TestDescription.uri)


@pytest.fixture(scope='session')
def deprecation():
    return Deprecation(TestDeprecation.target_album_id, TestDeprecation.status, TestDeprecation.done)


@pytest.fixture(scope='session')
def pager():
    return Pager(TestPager.total, TestPager.page, TestPager.per_page)


@pytest.fixture(scope='session')
def artist_event(artist, track):
    return ArtistEvent(artist, [track], [artist], TestArtistEvent.subscribed)


@pytest.fixture(scope='session')
def album_event(album, track):
    return AlbumEvent(album, [track])


@pytest.fixture(scope='session')
def video_supplement():
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
def ratings():
    return Ratings(TestRatings.month, TestRatings.week, TestRatings.day)


@pytest.fixture(scope='session')
def made_for(user, case_forms):
    return MadeFor(user, case_forms)


@pytest.fixture(scope='session')
def play_counter():
    return PlayCounter(TestPlayCounter.value, TestPlayCounter.description, TestPlayCounter.updated)


@pytest.fixture(scope='session')
def playlist_absence():
    return PlaylistAbsence(TestPlaylistAbsence.kind, TestPlaylistAbsence.reason)


@pytest.fixture(scope='session')
def results(playlist):
    return [playlist]


@pytest.fixture(scope='session')
def context():
    return Context(TestContext.type_, TestContext.id_, TestContext.description)


@pytest.fixture(scope='session')
def case_forms():
    return CaseForms(
        TestCaseForms.nominative,
        TestCaseForms.genitive,
        TestCaseForms.dative,
        TestCaseForms.accusative,
        TestCaseForms.instrumental,
        TestCaseForms.prepositional,
    )


@pytest.fixture(scope='session')
def lyrics():
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
def poetry_lover_match():
    return PoetryLoverMatch(TestPoetryLoverMatch.begin, TestPoetryLoverMatch.end, TestPoetryLoverMatch.line)


@pytest.fixture(scope='session')
def images():
    return Images(TestImages._208x208, TestImages._300x300)


@pytest.fixture(scope='session')
def normalization():
    return Normalization(TestNormalization.gain, TestNormalization.peak)


@pytest.fixture(scope='session')
def mix_link():
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
def title():
    return Title(TestTitle.title, TestTitle.full_title)


@pytest.fixture(scope='session')
def personal_playlists_data():
    return PersonalPlaylistsData(TestPersonalPlaylistsData.is_wizard_passed)


@pytest.fixture(scope='session')
def promotion():
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
def discrete_scale(value):
    return DiscreteScale(TestDiscreteScale.type, TestDiscreteScale.name, value, value)


@pytest.fixture(scope='session')
def major():
    return Major(TestMajor.id, TestMajor.name)


@pytest.fixture(scope='session')
def permissions():
    return Permissions(TestPermissions.until, TestPermissions.values, TestPermissions.default)


@pytest.fixture(scope='session')
def auto_renewable(product, user):
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
def passport_phone():
    return PassportPhone(TestPassportPhone.phone)


@pytest.fixture(scope='session')
def renewable_remainder():
    return RenewableRemainder(TestRenewableRemainder.days)


@pytest.fixture(scope='session')
def user():
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
def account(passport_phone):
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
    )


@pytest.fixture(scope='session')
def plus():
    return Plus(TestPlus.has_plus, TestPlus.is_tutorial_completed)


@pytest.fixture(scope='session')
def price():
    return Price(TestPrice.amount, TestPrice.currency)


@pytest.fixture(scope='session')
def subscription(renewable_remainder, auto_renewable, operator, non_auto_renewable):
    return Subscription(
        renewable_remainder,
        [auto_renewable],
        [auto_renewable],
        [operator],
        non_auto_renewable,
        TestSubscription.can_start_trial,
        TestSubscription.mcdonalds,
        TestSubscription.end,
    )


@pytest.fixture(scope='session')
def non_auto_renewable():
    return NonAutoRenewable(TestNonAutoRenewable.start, TestNonAutoRenewable.end)


@pytest.fixture(scope='session')
def deactivation():
    return Deactivation(TestDeactivation.method, TestDeactivation.instructions)


@pytest.fixture(scope='session')
def operator(deactivation):
    return Operator(
        TestOperator.product_id,
        TestOperator.phone,
        TestOperator.payment_regularity,
        [deactivation],
        TestOperator.title,
        TestOperator.suspended,
    )


@pytest.fixture(scope='session')
def rotor_settings():
    return RotorSettings(
        TestRotorSettings.language,
        TestRotorSettings.diversity,
        TestRotorSettings.mood,
        TestRotorSettings.energy,
        TestRotorSettings.mood_energy,
    )


@pytest.fixture(scope='session')
def product(price, licence_text_part):
    return Product(
        TestProduct.product_id,
        TestProduct.type,
        TestProduct.common_period_duration,
        TestProduct.duration,
        TestProduct.trial_duration,
        price,
        TestProduct.feature,
        TestProduct.debug,
        TestProduct.plus,
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
def playlist_id():
    return PlaylistId(TestPlaylistId.uid, TestPlaylistId.kind)


@pytest.fixture(scope='session')
def contest():
    return Contest(
        TestContest.contest_id, TestContest.status, TestContest.can_edit, TestContest.sent, TestContest.withdrawn
    )


@pytest.fixture(scope='session', params=[True, False])
def label(request):
    if request.param:
        return Label(TestLabel.id, TestLabel.name)

    return TestLabel.another_representation_of_label


@pytest.fixture(scope='session')
def track_position():
    return TrackPosition(TestTrackPosition.volume, TestTrackPosition.index)


@pytest.fixture(scope='session')
def status(account, permissions, subscription, plus, station_data, alert):
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
    )


@pytest.fixture(scope='session')
def station_data():
    return StationData(TestStationData.name)


@pytest.fixture(scope='session')
def alert_button():
    return AlertButton(TestAlertButton.text, TestAlertButton.bg_color, TestAlertButton.text_color, TestAlertButton.uri)


@pytest.fixture(scope='session')
def alert(alert_button):
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
def chart(track_id):
    return Chart(
        TestChart.position, TestChart.progress, TestChart.listeners, TestChart.shift, TestChart.bg_color, track_id
    )


@pytest.fixture(scope='session')
def event(track, artist_event, album_event):
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
def chart_info_menu_item():
    return ChartInfoMenuItem(TestChartInfoMenuItem.title, TestChartInfoMenuItem.url, TestChartInfoMenuItem.selected)


@pytest.fixture(scope='session')
def chart_info_menu(chart_info_menu_item):
    return ChartInfoMenu([chart_info_menu_item])


@pytest.fixture(scope='session')
def chart_info(playlist, chart_info_menu):
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
def track_id():
    return TrackId(TestTrackId.id, TestTrackId.track_id, TestTrackId.album_id, TestTrackId.from_)


@pytest.fixture(scope='session')
def value():
    return Value(TestValue.value, TestValue.name)


@pytest.fixture(scope='session')
def id_():
    return Id(TestId.type, TestId.tag)


@pytest.fixture(scope='session')
def sequence(track):
    return Sequence(TestSequence.type, track, TestSequence.liked)


@pytest.fixture(scope='session')
def station(id_, icon, restrictions):
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
    )


@pytest.fixture(scope='session')
def shot_type():
    return ShotType(TestShotType.id, TestShotType.title)


@pytest.fixture(scope='session')
def shot_data(shot_type):
    return ShotData(TestShotData.cover_uri, TestShotData.mds_url, TestShotData.shot_text, shot_type)


@pytest.fixture(scope='session')
def shot(shot_data):
    return Shot(TestShot.order, TestShot.played, shot_data, TestShot.shot_id, TestShot.status)


@pytest.fixture(scope='session')
def chart_item(track, chart):
    return ChartItem(track, chart)


@pytest.fixture(scope='session')
def station_result(station, rotor_settings, ad_params):
    return StationResult(
        station, rotor_settings, rotor_settings, ad_params, TestStationResult.explanation, TestStationResult.prerolls
    )


@pytest.fixture(scope='session')
def ad_params():
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
def restrictions(enum, discrete_scale):
    return Restrictions(enum, enum, discrete_scale, discrete_scale, enum)


@pytest.fixture(scope='session')
def results(
    track,
    artist,
    album,
    playlist,
    video,
    generated_playlist,
    promotion,
    chart_item,
    play_context,
    mix_link,
    personal_playlists_data,
    play_contexts_data,
    user,
):
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
def types():
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
def result_with_type(request, results, types):
    return results[request.param], types[request.param]


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5, 13, 14, 15])
def best(request, results, types):
    return Best(types[request.param], results[request.param], TestBest.text)


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5, 13, 14, 15])
def best_with_result(request, results, types):
    return Best(types[request.param], results[request.param], TestBest.text), results[request.param]


@pytest.fixture(scope='session', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity(request, results, types):
    return BlockEntity(TestBlockEntity.id, types[request.param], results[request.param])


@pytest.fixture(scope='session')
def block(block_entity, data_with_type):
    data, type_ = data_with_type

    return Block(
        TestBlock.id, type_, TestBlock.type_for_from, TestBlock.title, [block_entity], TestBlock.description, data
    )


@pytest.fixture(scope='session', params=[11, 12])
def data(request, results):
    return results[request.param]


@pytest.fixture(scope='session', params=[11, 12])
def data_with_type(request, results, types):
    return results[request.param], types[request.param]


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5])
def search_result_with_results_and_type(request, types, results):
    return (
        SearchResult(
            types[request.param],
            TestSearchResult.total,
            TestSearchResult.per_page,
            TestSearchResult.order,
            [results[request.param]],
        ),
        [results[request.param]],
        types[request.param],
    )
