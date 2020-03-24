import pytest

from yandex_music import Counts, TrackId, CaseForms, Ratings, Icon, Album, Lyrics, Track, InvocationInfo, Playlist, \
    AutoRenewable, Station, MadeFor, Normalization, Major, TrackPosition, Best, Chart, Restrictions, Permissions, \
    Product, Cover, PlayCounter, Sequence, Price, Artist, AdParams, Description, Subscription, Id, Images, Pager, \
    Account, Client, TrackShort, Value, DiscreteScale, PlaylistId, MixLink, Link, PassportPhone, User, Promotion, \
    PersonalPlaylistsData, RotorSettings, TrackShortOld, PlayContextsData, Status, Settings, StationResult, Enum, \
    TrackWithAds, VideoSupplement, ArtistEvent, ChartItem, Event, AlbumEvent, Day, PlayContext, Plus, Title, Label, \
    GeneratedPlaylist, Video, Vinyl, SearchResult, BlockEntity, Block, PlaylistAbsence, ShotType, ShotData, Shot
from . import TestCounts, TestTrackId, TestCaseForms, TestRatings, TestIcon, TestAlbum, TestLyrics, \
    TestTrack, TestInvocationInfo, TestPlaylist, TestAutoRenewable, TestStation, TestNormalization, TestMajor, \
    TestTrackPosition, TestBest, TestChart, TestPermissions, TestPlus, TestProduct, TestCover, TestPlayCounter, \
    TestSequence, TestPrice, TestArtist, TestAdParams, TestDescription, TestSubscription, TestId, TestImages, \
    TestDiscreteScale, TestAccount, TestTrackShort, TestEnum, TestValue, TestPlaylistId, TestMixLink, TestLink, \
    TestUser, TestPassportPhone, TestPromotion, TestTitle, TestPersonalPlaylistsData, TestRotorSettings, \
    TestTrackShortOld, TestPager, TestStatus, TestSettings, TestStationResult, TestLabel, TestTrackWithAds, \
    TestVideoSupplement, TestEvent, TestDay, TestPlayContext, TestGeneratedPlaylist, TestVideo, TestVinyl, \
    TestSearchResult, TestBlockEntity, TestBlock, TestPlaylistAbsence, TestShot, TestShotData, TestShotType


@pytest.fixture(scope='session')
def artist_factory(cover, counts, ratings, link, description):
    class ArtistFactory:
        def get(self, popular_tracks):
            return Artist(TestArtist.id, TestArtist.error, TestArtist.name, cover, TestArtist.various,
                          TestArtist.composer, TestArtist.genres, TestArtist.op_image,
                          TestArtist.no_pictures_from_search, counts, TestArtist.available, ratings, [link],
                          TestArtist.tickets_available, TestArtist.likes_count,  popular_tracks, TestArtist.regions,
                          TestArtist.decomposed, TestArtist.full_names, description, TestArtist.countries,
                          TestArtist.en_wikipedia_link, TestArtist.db_aliases, TestArtist.aliases, TestArtist.init_date,
                          TestArtist.end_date)

    return ArtistFactory()


@pytest.fixture(scope='session')
def artist(artist_factory, track_without_artists_and_albums):
    return artist_factory.get([track_without_artists_and_albums])


@pytest.fixture(scope='session')
def artist_without_tracks(artist_factory):
    return artist_factory.get([])


@pytest.fixture(scope='session')
def track_factory(major, normalization):
    class TrackFactory:
        def get(self, artists, albums):
            return Track(TestTrack.id, TestTrack.title, TestTrack.available, artists, albums,
                         TestTrack.available_for_premium_users, TestTrack.lyrics_available, TestTrack.real_id,
                         TestTrack.og_image, TestTrack.type, TestTrack.cover_uri, major, TestTrack.duration_ms,
                         TestTrack.storage_dir, TestTrack.file_size, normalization, TestTrack.error, TestTrack.regions,
                         TestTrack.available_as_rbt, TestTrack.content_warning, TestTrack.explicit,
                         TestTrack.preview_duration_ms, TestTrack.available_full_without_permission, TestTrack.version,
                         TestTrack.remember_position)

    return TrackFactory()


@pytest.fixture(scope='session')
def track(track_factory, artist, album):
    return track_factory.get([artist], [album])


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
def album_factory(label, track_position):
    class AlbumFactory:
        def get(self, artists, volumes):
            return Album(TestAlbum.id, TestAlbum.error, TestAlbum.title, TestAlbum.track_count, artists, [label],
                         TestAlbum.available, TestAlbum.available_for_premium_users, TestAlbum.version,
                         TestAlbum.cover_uri, TestAlbum.content_warning, TestAlbum.original_release_year,
                         TestAlbum.genre, TestAlbum.og_image, TestAlbum.buy, TestAlbum.recent, TestAlbum.very_important,
                         TestAlbum.available_for_mobile, TestAlbum.available_partially, TestAlbum.bests,
                         TestAlbum.prerolls, volumes, TestAlbum.year, TestAlbum.release_date, TestAlbum.type,
                         track_position, TestAlbum.regions)

    return AlbumFactory()


@pytest.fixture(scope='session')
def album(album_factory, artist_without_tracks, track_without_albums):
    return album_factory.get([artist_without_tracks], [[track_without_albums]])


@pytest.fixture(scope='session')
def album_without_tracks(album_factory, artist_without_tracks):
    return album_factory.get([artist_without_tracks], [])


@pytest.fixture(scope='session')
def playlist_factory(user, cover, made_for, track_short, play_counter, playlist_absence):
    class PlaylistFactory:
        def get(self):
            return Playlist(user, cover, made_for, play_counter, playlist_absence, TestPlaylist.uid, TestPlaylist.kind,
                            TestPlaylist.title, TestPlaylist.track_count, TestPlaylist.tags, TestPlaylist.revision,
                            TestPlaylist.snapshot, TestPlaylist.visibility, TestPlaylist.collective,
                            TestPlaylist.created, TestPlaylist.modified, TestPlaylist.available, TestPlaylist.is_banner,
                            TestPlaylist.is_premiere, TestPlaylist.duration_ms, TestPlaylist.og_image, [track_short],
                            TestPlaylist.prerolls, TestPlaylist.likes_count, TestPlaylist.generated_playlist_type,
                            TestPlaylist.animated_cover_uri, TestPlaylist.ever_played, TestPlaylist.description,
                            TestPlaylist.description_formatted, TestPlaylist.is_for_from, TestPlaylist.regions)

    return PlaylistFactory()


@pytest.fixture(scope='session')
def playlist(playlist_factory):
    return playlist_factory.get()


@pytest.fixture(scope='session')
def generated_playlist(playlist):
    return GeneratedPlaylist(TestGeneratedPlaylist.type, TestGeneratedPlaylist.ready,
                             TestGeneratedPlaylist.notify, playlist)


@pytest.fixture(scope='session')
def client():
    return Client()


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
    return Video(TestVideo.title, TestVideo.cover, TestVideo.embed_url, TestVideo.provider, TestVideo.provider_video_id,
                 TestVideo.youtube_url, TestVideo.thumbnail_url, TestVideo.duration, TestVideo.text,
                 TestVideo.html_auto_play_video_player, TestVideo.regions)


@pytest.fixture(scope='session')
def vinyl():
    return Vinyl(TestVinyl.url, TestVinyl.title, TestVinyl.year, TestVinyl.price, TestVinyl.media, TestVinyl.picture)


@pytest.fixture(scope='session')
def play_context(track_short_old):
    return PlayContext(TestPlayContext.client_, TestPlayContext.context,
                       TestPlayContext.context_item, [track_short_old])


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
    return Cover(TestCover.type, TestCover.uri, TestCover.items_uri, TestCover.dir,
                 TestCover.version, TestCover.custom, TestCover.prefix, TestCover.error)


@pytest.fixture(scope='session')
def link():
    return Link(TestLink.title, TestLink.href, TestLink.type, TestLink.social_network)


@pytest.fixture(scope='session')
def invocation_info():
    return InvocationInfo(TestInvocationInfo.hostname, TestInvocationInfo.req_id,
                          TestInvocationInfo.exec_duration_millis)


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
def pager():
    return Pager(TestPager.total, TestPager.page, TestPager.per_page)


@pytest.fixture(scope='session')
def artist_event(artist, track):
    return ArtistEvent(artist, [track], [artist])


@pytest.fixture(scope='session')
def album_event(album, track):
    return AlbumEvent(album, [track])


@pytest.fixture(scope='session')
def video_supplement():
    return VideoSupplement(TestVideoSupplement.cover, TestVideoSupplement.title, TestVideoSupplement.provider,
                           TestVideoSupplement.provider_video_id, TestVideoSupplement.url,
                           TestVideoSupplement.embed_url, TestVideoSupplement.embed)


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
def case_forms():
    return CaseForms(TestCaseForms.nominative, TestCaseForms.genitive, TestCaseForms.dative,
                     TestCaseForms.accusative, TestCaseForms.instrumental, TestCaseForms.prepositional)


@pytest.fixture(scope='session')
def lyrics():
    return Lyrics(TestLyrics.id, TestLyrics.lyrics, TestLyrics.full_lyrics, TestLyrics.has_rights,
                  TestLyrics.text_language, TestLyrics.show_translation)


@pytest.fixture(scope='session')
def images():
    return Images(TestImages._208x208, TestImages._300x300)


@pytest.fixture(scope='session')
def normalization():
    return Normalization(TestNormalization.gain, TestNormalization.peak)


@pytest.fixture(scope='session')
def mix_link():
    return MixLink(TestMixLink.title, TestMixLink.url, TestMixLink.url_scheme, TestMixLink.text_color,
                   TestMixLink.background_color, TestMixLink.background_image_uri, TestMixLink.cover_white)


@pytest.fixture(scope='session')
def title():
    return Title(TestTitle.title, TestTitle.full_title)


@pytest.fixture(scope='session')
def personal_playlists_data():
    return PersonalPlaylistsData(TestPersonalPlaylistsData.is_wizard_passed)


@pytest.fixture(scope='session')
def promotion():
    return Promotion(TestPromotion.promo_id, TestPromotion.title, TestPromotion.subtitle, TestPromotion.heading,
                     TestPromotion.url, TestPromotion.url_scheme, TestPromotion.text_color, TestPromotion.gradient,
                     TestPromotion.image)


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
def auto_renewable(product):
    return AutoRenewable(TestAutoRenewable.expires, TestAutoRenewable.vendor, TestAutoRenewable.vendor_help_url,
                         product, TestAutoRenewable.finished, TestAutoRenewable.product_id, TestAutoRenewable.order_id)


@pytest.fixture(scope='session')
def passport_phone():
    return PassportPhone(TestPassportPhone.phone)


@pytest.fixture(scope='session')
def user():
    return User(TestUser.uid, TestUser.login, TestUser.name, TestUser.sex, TestUser.verified)


@pytest.fixture(scope='session')
def account(passport_phone):
    return Account(TestAccount.now, TestAccount.service_available, TestAccount.region, TestAccount.uid,
                   TestAccount.login, TestAccount.full_name, TestAccount.second_name, TestAccount.first_name,
                   TestAccount.display_name, TestAccount.hosted_user, TestAccount.birthday, [passport_phone],
                   TestAccount.registered_at, TestAccount.has_info_for_app_metrica)


@pytest.fixture(scope='session')
def plus():
    return Plus(TestPlus.has_plus, TestPlus.is_tutorial_completed)


@pytest.fixture(scope='session')
def price():
    return Price(TestPrice.amount, TestPrice.currency)


@pytest.fixture(scope='session')
def subscription(auto_renewable):
    return Subscription([auto_renewable], TestSubscription.can_start_trial, TestSubscription.mcdonalds,
                        TestSubscription.end)


@pytest.fixture(scope='session')
def rotor_settings():
    return RotorSettings(TestRotorSettings.language, TestRotorSettings.diversity, TestRotorSettings.mood,
                         TestRotorSettings.energy, TestRotorSettings.mood_energy)


@pytest.fixture(scope='session')
def product(price):
    return Product(TestProduct.product_id, TestProduct.type, TestProduct.common_period_duration, TestProduct.duration,
                   TestProduct.trial_duration, price, TestProduct.feature, TestProduct.debug, TestProduct.features,
                   TestProduct.description, TestProduct.available, TestProduct.trial_available,
                   TestProduct.vendor_trial_available, TestProduct.button_text, TestProduct.button_additional_text,
                   TestProduct.payment_method_types)


@pytest.fixture(scope='session')
def playlist_id():
    return PlaylistId(TestPlaylistId.uid, TestPlaylistId.kind)


@pytest.fixture(scope='session')
def label():
    return Label(TestLabel.id, TestLabel.name)


@pytest.fixture(scope='session')
def track_position():
    return TrackPosition(TestTrackPosition.volume, TestTrackPosition.index)


@pytest.fixture(scope='session')
def status(account, permissions, subscription, plus):
    return Status(account, permissions, subscription, TestStatus.cache_limit, TestStatus.subeditor,
                  TestStatus.subeditor_level, plus, TestStatus.default_email, TestStatus.skips_per_hour,
                  TestStatus.station_exists, TestStatus.premium_region)


@pytest.fixture(scope='session')
def chart(track_id):
    return Chart(TestChart.position, TestChart.progress, TestChart.listeners, TestChart.shift, track_id)


@pytest.fixture(scope='session')
def event(track, artist_event, album_event):
    return Event(TestEvent.id, TestEvent.type, TestEvent.type_for_from, TestEvent.title, [track], [artist_event],
                 [album_event], TestEvent.message, TestEvent.device, TestEvent.tracks_count)


@pytest.fixture(scope='session')
def track_id():
    return TrackId(TestTrackId.id, TestTrackId.album_id)


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
    return Station(id_, TestStation.name, icon, icon, icon, TestStation.id_for_from, restrictions, restrictions, id_)


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
    return StationResult(station, rotor_settings, rotor_settings, ad_params, TestStationResult.explanation,
                         TestStationResult.prerolls)


@pytest.fixture(scope='session')
def ad_params():
    return AdParams(TestAdParams.partner_id, TestAdParams.category_id, TestAdParams.page_ref, TestAdParams.target_ref,
                    TestAdParams.other_params, TestAdParams.ad_volume, TestAdParams.genre_id, TestAdParams.genre_name)


@pytest.fixture(scope='session')
def restrictions(enum, discrete_scale):
    return Restrictions(enum, enum, discrete_scale, discrete_scale, enum)


@pytest.fixture(scope='session')
def results(track, artist, album, playlist, video, generated_playlist, promotion, chart_item, play_context, mix_link,
            personal_playlists_data, play_contexts_data):
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
        12: play_contexts_data
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
        12: 'play-contexts'
    }


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5])
def result_with_type(request, results, types):
    return results[request.param], types[request.param]


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5])
def best(request, results, types):
    return Best(types[request.param], results[request.param], TestBest.text)


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5])
def best_with_result(request, results, types):
    return Best(types[request.param], results[request.param], TestBest.text), results[request.param]


@pytest.fixture(scope='session', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity(request, results, types):
    return BlockEntity(TestBlockEntity.id, types[request.param], results[request.param])


@pytest.fixture(scope='session')
def block(block_entity, data_with_type):
    data, type_ = data_with_type

    return Block(TestBlock.id, type_, TestBlock.type_for_from, TestBlock.title, [block_entity],
                 TestBlock.description, data)


@pytest.fixture(scope='session', params=[11, 12])
def data(request, results):
    return results[request.param]


@pytest.fixture(scope='session', params=[11, 12])
def data_with_type(request, results, types):
    return results[request.param], types[request.param]


@pytest.fixture(scope='session', params=[1, 2, 3, 4, 5])
def search_result_with_results_and_type(request, types, results):
    return SearchResult(types[request.param], TestSearchResult.total, TestSearchResult.per_page, TestSearchResult.order,
                        [results[request.param]]), [results[request.param]], types[request.param]
