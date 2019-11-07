import pytest

from yandex_music import Counts, TrackId, CaseForms, Ratings, Icon, Album, Lyrics, Track, \
    InvocationInfo, Playlist, AutoRenewable, Station, MadeFor, Normalization, Major, TrackPosition, Best, Chart, \
    Restrictions, Permissions, Plus, Product, Cover, \
    PlayCounter, Sequence, Price, Artist, AdParams, Description, Subscription, Id, Images, \
    Pager, Account, Client, TrackShort
from . import TestCounts, TestTrackId, TestCaseForms, TestRatings, TestIcon, TestAlbum, TestLyrics, \
    TestTrack, TestInvocationInfo, TestPlaylist, TestAutoRenewable, TestStation, TestNormalization, TestMajor, \
    TestTrackPosition, TestBest, TestChart, TestRestrictions, \
    TestPermissions, TestPlus, TestProduct, TestCover, TestPlayCounter, TestSequence, TestPrice, TestArtist, \
    TestAdParams, TestDescription, TestSubscription, \
    TestId, TestImages, TestPager, TestAccount, TestTrackShort


@pytest.fixture(scope='session')
def client():
    return Client()


@pytest.fixture(scope='session')
def track_short():
    return TrackShort(TestTrackShort.id, TestTrackShort.timestamp, TestTrackShort.album_id)


@pytest.fixture(scope='session')
def icon():
    return Icon(TestIcon.background_color, TestIcon.image_url)


@pytest.fixture(scope='session')
def cover():
    return Cover(TestCover.type, TestCover.uri, TestCover.items_uri, TestCover.dir, TestCover.version, TestCover.custom,
                 TestCover.prefix, TestCover.error)


@pytest.fixture(scope='session')
def all_covers(cover):
    return [cover]


@pytest.fixture(scope='session')
def invocation_info():
    return InvocationInfo(TestInvocationInfo.hostname, TestInvocationInfo.req_id,
                          TestInvocationInfo.exec_duration_millis)


@pytest.fixture(scope='session')
def settings(in_app_products, native_products):
    return Settings(in_app_products, native_products, TestSettings.web_payment_url, TestSettings.promo_codes_enabled,
                    TestSettings.web_payment_month_product_price)


@pytest.fixture(scope='session')
def counts(tracks, also_albums):
    return Counts(tracks, TestCounts.direct_albums, also_albums, TestCounts.also_tracks)


@pytest.fixture(scope='session')
def description():
    return Description(TestDescription.text, TestDescription.url)


@pytest.fixture(scope='session')
def pager():
    return Pager(TestPager.total, TestPager.page, TestPager.per_page)


@pytest.fixture(scope='session')
def artist(id, cover, counts, ratings, links, popular_tracks, description):
    return Artist(id, TestArtist.name, TestArtist.various, TestArtist.composer, cover, TestArtist.genres,
                  TestArtist.op_image, TestArtist.no_pictures_from_search, counts, TestArtist.available, ratings, links,
                  TestArtist.tickets_available, TestArtist.likes_count, popular_tracks, TestArtist.regions,
                  TestArtist.decomposed, TestArtist.full_names, description, TestArtist.countries,
                  TestArtist.en_wikipedia_link, TestArtist.db_aliases, TestArtist.aliases, TestArtist.init_date,
                  TestArtist.end_date)


@pytest.fixture(scope='session')
def artists(artist):
    return [artist]


@pytest.fixture(scope='session')
def artists(artist):
    return [artist]


@pytest.fixture(scope='session')
def results(artist):
    return [artist]


@pytest.fixture(scope='session')
def similar_to_artists_from_history(artist):
    return [artist]


@pytest.fixture(scope='session')
def ratings():
    return Ratings(TestRatings.week, TestRatings.month, TestRatings.day)


@pytest.fixture(scope='session')
def made_for(user_info, case_forms):
    return MadeFor(user_info, case_forms)


@pytest.fixture(scope='session')
def play_counter(description):
    return PlayCounter(TestPlayCounter.value, description, TestPlayCounter.updated)


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
def lyrics(id):
    return Lyrics(id, lyrics, TestLyrics.full_lyrics, TestLyrics.has_rights, TestLyrics.text_language,
                  TestLyrics.show_translation)


@pytest.fixture(scope='session')
def images():
    return Images(TestImages._208x208, TestImages._300x300)


@pytest.fixture(scope='session')
def normalization():
    return Normalization(TestNormalization.gain, TestNormalization.peak)


@pytest.fixture(scope='session')
def major(id):
    return Major(id, TestMajor.name)


@pytest.fixture(scope='session')
def track(id, artists, albums, major, normalization):
    return Track(id, TestTrack.title, TestTrack.available, TestTrack.available_for_premium_users, artists, albums,
                 TestTrack.lyrics_available, TestTrack.real_id, TestTrack.og_image, TestTrack.type, TestTrack.cover_uri,
                 major, TestTrack.duration_ms, TestTrack.storage_dir, TestTrack.file_size, normalization,
                 TestTrack.error, TestTrack.regions, TestTrack.available_as_rbt, TestTrack.content_warning,
                 TestTrack.explicit, TestTrack.preview_duration_ms, TestTrack.available_full_without_permission)


@pytest.fixture(scope='session')
def popular_tracks(track):
    return [track]


@pytest.fixture(scope='session')
def popular_tracks(track):
    return [track]


@pytest.fixture(scope='session')
def tracks(track):
    return [track]


@pytest.fixture(scope='session')
def results(track):
    return [track]


@pytest.fixture(scope='session')
def tracks(track):
    return [track]


@pytest.fixture(scope='session')
def tracks(track):
    return [track]


@pytest.fixture(scope='session')
def tracks(track):
    return [track]


@pytest.fixture(scope='session')
def tracks_to_play(track):
    return [track]


@pytest.fixture(scope='session')
def permissions():
    return Permissions(TestPermissions.until, TestPermissions.values, TestPermissions.default)


@pytest.fixture(scope='session')
def auto_renewable(product):
    return AutoRenewable(TestAutoRenewable.expires, TestAutoRenewable.vendor, TestAutoRenewable.vendor_help_url,
                         TestAutoRenewable.product_id, product, TestAutoRenewable.finished, TestAutoRenewable.order_id)


@pytest.fixture(scope='session')
def auto_renewable(auto_renewable):
    return [auto_renewable]


@pytest.fixture(scope='session')
def account(passport_phones):
    return Account(TestAccount.now, TestAccount.region, TestAccount.service_available, TestAccount.uid,
                   TestAccount.login, TestAccount.full_name, TestAccount.second_name, TestAccount.first_name,
                   TestAccount.display_name, TestAccount.hosted_user, TestAccount.birthday, passport_phones,
                   TestAccount.registered_at, TestAccount.has_info_for_app_metrica)


@pytest.fixture(scope='session')
def plus():
    return Plus(TestPlus.has_plus, TestPlus.is_tutorial_completed)


@pytest.fixture(scope='session')
def price():
    return Price(TestPrice.amount, TestPrice.currency)


@pytest.fixture(scope='session')
def subscription(auto_renewable):
    return Subscription(auto_renewable, TestSubscription.can_start_trial, TestSubscription.mcdonalds,
                        TestSubscription.end)


@pytest.fixture(scope='session')
def product(price, description):
    return Product(TestProduct.product_id, TestProduct.type, TestProduct.common_period_duration, TestProduct.duration,
                   TestProduct.trial_duration, price, TestProduct.feature, TestProduct.debug, TestProduct.features,
                   description, TestProduct.available, TestProduct.trial_available, TestProduct.vendor_trial_available,
                   TestProduct.button_text, TestProduct.button_additional_text, TestProduct.payment_method_types)


@pytest.fixture(scope='session')
def in_app_products(product):
    return [product]


@pytest.fixture(scope='session')
def native_products(product):
    return [product]


@pytest.fixture(scope='session')
def album(id, artists, labels, track_position):
    return Album(id, TestAlbum.title, TestAlbum.cover_uri, TestAlbum.track_count, artists, labels, TestAlbum.available,
                 TestAlbum.available_for_premium_users, TestAlbum.content_warning, TestAlbum.original_release_year,
                 TestAlbum.genre, TestAlbum.og_image, TestAlbum.buy, TestAlbum.recent, TestAlbum.very_important,
                 TestAlbum.available_for_mobile, TestAlbum.available_partially, TestAlbum.bests, TestAlbum.prerolls,
                 TestAlbum.volumes, TestAlbum.year, TestAlbum.release_date, TestAlbum.type, track_position,
                 TestAlbum.regions)


@pytest.fixture(scope='session')
def albums(album):
    return [album]


@pytest.fixture(scope='session')
def also_albums(album):
    return [album]


@pytest.fixture(scope='session')
def albums(album):
    return [album]


@pytest.fixture(scope='session')
def results(album):
    return [album]


@pytest.fixture(scope='session')
def track_position():
    return TrackPosition(TestTrackPosition.volume, TestTrackPosition.index)


@pytest.fixture(scope='session')
def best():
    return Best(TestBest.type, TestBest.result, TestBest.text)


@pytest.fixture(scope='session')
def chart(track_id):
    return Chart(TestChart.position, TestChart.progress, TestChart.listeners, TestChart.shift, track_id)


@pytest.fixture(scope='session')
def tracks_in_chart(chart):
    return [chart]


@pytest.fixture(scope='session')
def track_id(id):
    return TrackId(id, TestTrackId.album_id)


@pytest.fixture(scope='session')
def id():
    return Id(TestId.type, TestId.tag)


@pytest.fixture(scope='session')
def sequence(track):
    return Sequence(TestSequence.type, track, TestSequence.liked)


@pytest.fixture(scope='session')
def sequence(sequence):
    return [sequence]


@pytest.fixture(scope='session')
def station(id, icon, mts_icon, geocell_icon, restrictions, restrictions2, parent_id):
    return Station(id, TestStation.name, icon, mts_icon, geocell_icon, TestStation.id_for_from, restrictions,
                   restrictions2, parent_id)


@pytest.fixture(scope='session')
def ad_params():
    return AdParams(TestAdParams.partner_id, TestAdParams.category_id, TestAdParams.page_ref, TestAdParams.target_ref,
                    TestAdParams.other_params, TestAdParams.ad_volume, TestAdParams.genre_id, TestAdParams.genre_name)


@pytest.fixture(scope='session')
def restrictions():
    return Restrictions(TestRestrictions.language, TestRestrictions.diversity, TestRestrictions.mood,
                        TestRestrictions.energy, TestRestrictions.mood_energy)
