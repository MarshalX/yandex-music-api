import pytest

from yandex_music import Counts, TrackId, CaseForms, Ratings, Icon, Album, Lyrics, Track, \
    InvocationInfo, Playlist, AutoRenewable, Station, MadeFor, Normalization, Major, TrackPosition, Best, Chart, \
    Restrictions, Permissions, Plus, Product, Cover, PlayCounter, Sequence, Price, Artist, AdParams, Description, \
    Subscription, Id, Images, Pager, Account, Client, TrackShort, Value, DiscreteScale, PlaylistId, MixLink, Link, \
    PassportPhone, User, Promotion, Title, PersonalPlaylistsData, RotorSettings, TrackShortOld, PlayContextsData, \
    Status, Settings, StationResult, Enum, Label
from . import TestCounts, TestTrackId, TestCaseForms, TestRatings, TestIcon, TestAlbum, TestLyrics, \
    TestTrack, TestInvocationInfo, TestPlaylist, TestAutoRenewable, TestStation, TestNormalization, TestMajor, \
    TestTrackPosition, TestBest, TestChart, TestPermissions, TestPlus, TestProduct, TestCover, \
    TestPlayCounter, TestSequence, TestPrice, TestArtist, TestAdParams, TestDescription, TestSubscription, TestId, \
    TestImages, TestPager, TestAccount, TestTrackShort, TestValue, TestDiscreteScale, TestPlaylistId, TestMixLink, \
    TestLink, TestPassportPhone, TestUser, TestPromotion, TestTitle, TestPersonalPlaylistsData, TestRotorSettings, \
    TestTrackShortOld, TestEnum, TestStatus, TestSettings, TestStationResult, TestLabel


@pytest.fixture(scope='session')
def client():
    return Client()


@pytest.fixture(scope='session')
def track_short():
    return TrackShort(TestTrackShort.id, TestTrackShort.timestamp, TestTrackShort.album_id)


@pytest.fixture(scope='session')
def track_short_old(track_id):
    return TrackShortOld(track_id, TestTrackShortOld.timestamp)


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
    return Cover(TestCover.type, TestCover.uri, TestCover.items_uri, TestCover.dir, TestCover.version, TestCover.custom,
                 TestCover.prefix, TestCover.error)


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
    return Description(TestDescription.text, TestDescription.url)


@pytest.fixture(scope='session')
def pager():
    return Pager(TestPager.total, TestPager.page, TestPager.per_page)


@pytest.fixture(scope='session')
def artist(cover, counts, ratings, link, track, description):
    return Artist(TestArtist.id, TestArtist.name, TestArtist.various, TestArtist.composer, cover, TestArtist.genres,
                  TestArtist.op_image, TestArtist.no_pictures_from_search, counts, TestArtist.available, ratings,
                  [link], TestArtist.tickets_available, TestArtist.likes_count, [track], TestArtist.regions,
                  TestArtist.decomposed, TestArtist.full_names, description, TestArtist.countries,
                  TestArtist.en_wikipedia_link, TestArtist.db_aliases, TestArtist.aliases, TestArtist.init_date,
                  TestArtist.end_date)


@pytest.fixture(scope='session')
def artist_without_tracks(cover, counts, ratings, link, description):
    return Artist(TestArtist.id, TestArtist.name, TestArtist.various, TestArtist.composer, cover, TestArtist.genres,
                  TestArtist.op_image, TestArtist.no_pictures_from_search, counts, TestArtist.available, ratings,
                  [link], TestArtist.tickets_available, TestArtist.likes_count, [], TestArtist.regions,
                  TestArtist.decomposed, TestArtist.full_names, description, TestArtist.countries,
                  TestArtist.en_wikipedia_link, TestArtist.db_aliases, TestArtist.aliases, TestArtist.init_date,
                  TestArtist.end_date)


@pytest.fixture(scope='session')
def track(artist_without_tracks, album_without_tracks, major, normalization):
    return Track(TestTrack.id, TestTrack.title, TestTrack.available, TestTrack.available_for_premium_users,
                 [artist_without_tracks], [album_without_tracks], TestTrack.lyrics_available, TestTrack.real_id,
                 TestTrack.og_image, TestTrack.type, TestTrack.cover_uri, major, TestTrack.duration_ms,
                 TestTrack.storage_dir, TestTrack.file_size, normalization, TestTrack.error, TestTrack.regions,
                 TestTrack.available_as_rbt, TestTrack.content_warning, TestTrack.explicit,
                 TestTrack.preview_duration_ms, TestTrack.available_full_without_permission)


@pytest.fixture(scope='session')
def track_without_artists(album_without_tracks, major, normalization):
    return Track(TestTrack.id, TestTrack.title, TestTrack.available, TestTrack.available_for_premium_users, [],
                 [album_without_tracks], TestTrack.lyrics_available, TestTrack.real_id, TestTrack.og_image,
                 TestTrack.type, TestTrack.cover_uri, major, TestTrack.duration_ms, TestTrack.storage_dir,
                 TestTrack.file_size, normalization, TestTrack.error, TestTrack.regions, TestTrack.available_as_rbt,
                 TestTrack.content_warning, TestTrack.explicit, TestTrack.preview_duration_ms,
                 TestTrack.available_full_without_permission)


@pytest.fixture(scope='session')
def track_without_albums(artist, major, normalization):
    return Track(TestTrack.id, TestTrack.title, TestTrack.available, TestTrack.available_for_premium_users,
                 [artist], [], TestTrack.lyrics_available, TestTrack.real_id, TestTrack.og_image, TestTrack.type,
                 TestTrack.cover_uri, major, TestTrack.duration_ms, TestTrack.storage_dir, TestTrack.file_size,
                 normalization, TestTrack.error, TestTrack.regions, TestTrack.available_as_rbt,
                 TestTrack.content_warning, TestTrack.explicit, TestTrack.preview_duration_ms,
                 TestTrack.available_full_without_permission)


@pytest.fixture(scope='session')
def album(artist, label, track_position, track):
    return Album(TestAlbum.id, TestAlbum.title, TestAlbum.track_count, [artist], [label],
                 TestAlbum.available, TestAlbum.available_for_premium_users, TestAlbum.cover_uri,
                 TestAlbum.content_warning, TestAlbum.original_release_year, TestAlbum.genre, TestAlbum.og_image,
                 TestAlbum.buy, TestAlbum.recent, TestAlbum.very_important, TestAlbum.available_for_mobile,
                 TestAlbum.available_partially, TestAlbum.bests, TestAlbum.prerolls, [[track]], TestAlbum.year,
                 TestAlbum.release_date, TestAlbum.type, track_position, TestAlbum.regions)


@pytest.fixture(scope='session')
def album_without_tracks(artist_without_tracks, label, track_position):
    return Album(TestAlbum.id, TestAlbum.title, TestAlbum.track_count, [artist_without_tracks], [label],
                 TestAlbum.available, TestAlbum.available_for_premium_users, TestAlbum.cover_uri,
                 TestAlbum.content_warning, TestAlbum.original_release_year, TestAlbum.genre, TestAlbum.og_image,
                 TestAlbum.buy, TestAlbum.recent, TestAlbum.very_important, TestAlbum.available_for_mobile,
                 TestAlbum.available_partially, TestAlbum.bests, TestAlbum.prerolls, [[]], TestAlbum.year,
                 TestAlbum.release_date, TestAlbum.type, track_position, TestAlbum.regions)


@pytest.fixture(scope='session')
def ratings():
    return Ratings(TestRatings.week, TestRatings.month, TestRatings.day)


@pytest.fixture(scope='session')
def made_for(user, case_forms):
    return MadeFor(user, case_forms)


@pytest.fixture(scope='session')
def play_counter():
    return PlayCounter(TestPlayCounter.value, TestPlayCounter.description, TestPlayCounter.updated)


@pytest.fixture(scope='session')
def playlist(owner, cover, made_for, play_counter, tracks, description):
    return Playlist(owner, TestPlaylist.uid, TestPlaylist.kind, TestPlaylist.title, TestPlaylist.track_count, cover,
                    made_for, play_counter, TestPlaylist.tags, TestPlaylist.revision, TestPlaylist.snapshot,
                    TestPlaylist.visibility, TestPlaylist.collective, TestPlaylist.created, TestPlaylist.modified,
                    TestPlaylist.available, TestPlaylist.is_banner, TestPlaylist.is_premiere, TestPlaylist.duration_ms,
                    TestPlaylist.og_image, tracks, TestPlaylist.prerolls, TestPlaylist.likes_count,
                    TestPlaylist.generated_playlist_type, TestPlaylist.animated_cover_uri, TestPlaylist.ever_played,
                    description, TestPlaylist.description_formatted, TestPlaylist.is_for_from, TestPlaylist.regions)


@pytest.fixture(scope='session')
def results(playlist):
    return [playlist]


@pytest.fixture(scope='session')
def case_forms():
    return CaseForms(TestCaseForms.nominative, TestCaseForms.genitive, TestCaseForms.dative, TestCaseForms.accusative,
                     TestCaseForms.instrumental, TestCaseForms.prepositional)


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
                         TestAutoRenewable.product_id, product, TestAutoRenewable.finished, TestAutoRenewable.order_id)


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
def best():
    return Best(TestBest.type, TestBest.result, TestBest.text)


@pytest.fixture(scope='session')
def status(account, permissions, subscription, plus):
    return Status(account, permissions, subscription, TestStatus.cache_limit, TestStatus.subeditor,
                  TestStatus.subeditor_level, plus, TestStatus.default_email, TestStatus.skips_per_hour,
                  TestStatus.station_exists, TestStatus.premium_region)


@pytest.fixture(scope='session')
def chart(track_id):
    return Chart(TestChart.position, TestChart.progress, TestChart.listeners, TestChart.shift, track_id)


@pytest.fixture(scope='session')
def track_id():
    return TrackId(TestTrackId.id, TestTrackId.album_id)


@pytest.fixture(scope='session')
def value():
    return Value(TestValue.value, TestValue.name)


@pytest.fixture(scope='session')
def id():
    return Id(TestId.type, TestId.tag)


@pytest.fixture(scope='session')
def sequence(track):
    return Sequence(TestSequence.type, track, TestSequence.liked)


@pytest.fixture(scope='session')
def station(id, icon, restrictions):
    return Station(id, TestStation.name, icon, icon, icon, TestStation.id_for_from, restrictions, restrictions, id)


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
