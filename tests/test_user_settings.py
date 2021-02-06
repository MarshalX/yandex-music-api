import pytest

from yandex_music import UserSettings


@pytest.fixture(scope='class')
def user_settings(shot):
    return UserSettings(
        TestUserSettings.uid,
        TestUserSettings.last_fm_scrobbling_enabled,
        TestUserSettings.shuffle_enabled,
        TestUserSettings.volume_percents,
        TestUserSettings.modified,
        TestUserSettings.facebook_scrobbling_enabled,
        TestUserSettings.add_new_track_on_playlist_top,
        TestUserSettings.user_music_visibility,
        TestUserSettings.user_social_visibility,
        TestUserSettings.rbt_disabled,
        TestUserSettings.theme,
        TestUserSettings.promos_disabled,
        TestUserSettings.auto_play_radio,
        TestUserSettings.sync_queue_enabled,
        TestUserSettings.ads_disabled,
        TestUserSettings.disk_enabled,
        TestUserSettings.show_disk_tracks_in_library,
    )


class TestUserSettings:
    uid = 1130000002804400
    last_fm_scrobbling_enabled = False
    shuffle_enabled = False
    volume_percents = 70
    modified = '2020-01-25T22:52:21+00:00'
    facebook_scrobbling_enabled = False
    add_new_track_on_playlist_top = False
    user_music_visibility = 'public'
    user_social_visibility = 'public'
    rbt_disabled = False
    theme = 'black'
    promos_disabled = True
    auto_play_radio = True
    sync_queue_enabled = True
    ads_disabled = None
    disk_enabled = False
    show_disk_tracks_in_library = False

    def test_expected_values(self, user_settings):
        assert user_settings.uid == self.uid
        assert user_settings.last_fm_scrobbling_enabled == self.last_fm_scrobbling_enabled
        assert user_settings.shuffle_enabled == self.shuffle_enabled
        assert user_settings.volume_percents == self.volume_percents
        assert user_settings.modified == self.modified
        assert user_settings.facebook_scrobbling_enabled == self.facebook_scrobbling_enabled
        assert user_settings.add_new_track_on_playlist_top == self.add_new_track_on_playlist_top
        assert user_settings.user_music_visibility == self.user_music_visibility
        assert user_settings.user_social_visibility == self.user_social_visibility
        assert user_settings.rbt_disabled == self.rbt_disabled
        assert user_settings.theme == self.theme
        assert user_settings.promos_disabled == self.promos_disabled
        assert user_settings.auto_play_radio == self.auto_play_radio
        assert user_settings.sync_queue_enabled == self.sync_queue_enabled
        assert user_settings.ads_disabled == self.ads_disabled
        assert user_settings.disk_enabled == self.disk_enabled
        assert user_settings.show_disk_tracks_in_library == self.show_disk_tracks_in_library

    def test_de_json_none(self, client):
        assert UserSettings.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'uid': self.uid,
            'last_fm_scrobbling_enabled': self.last_fm_scrobbling_enabled,
            'shuffle_enabled': self.shuffle_enabled,
            'volume_percents': self.volume_percents,
            'modified': self.modified,
            'facebook_scrobbling_enabled': self.facebook_scrobbling_enabled,
            'add_new_track_on_playlist_top': self.add_new_track_on_playlist_top,
            'user_music_visibility': self.user_music_visibility,
            'user_social_visibility': self.user_social_visibility,
            'rbt_disabled': self.rbt_disabled,
            'theme': self.theme,
            'promos_disabled': self.promos_disabled,
            'auto_play_radio': self.auto_play_radio,
            'sync_queue_enabled': self.sync_queue_enabled,
        }
        user_settings = UserSettings.de_json(json_dict, client)

        assert user_settings.uid == self.uid
        assert user_settings.last_fm_scrobbling_enabled == self.last_fm_scrobbling_enabled
        assert user_settings.shuffle_enabled == self.shuffle_enabled
        assert user_settings.volume_percents == self.volume_percents
        assert user_settings.modified == self.modified
        assert user_settings.facebook_scrobbling_enabled == self.facebook_scrobbling_enabled
        assert user_settings.add_new_track_on_playlist_top == self.add_new_track_on_playlist_top
        assert user_settings.user_music_visibility == self.user_music_visibility
        assert user_settings.user_social_visibility == self.user_social_visibility
        assert user_settings.rbt_disabled == self.rbt_disabled
        assert user_settings.theme == self.theme
        assert user_settings.promos_disabled == self.promos_disabled
        assert user_settings.auto_play_radio == self.auto_play_radio
        assert user_settings.sync_queue_enabled == self.sync_queue_enabled

    def test_de_json_all(self, client):
        json_dict = {
            'uid': self.uid,
            'last_fm_scrobbling_enabled': self.last_fm_scrobbling_enabled,
            'shuffle_enabled': self.shuffle_enabled,
            'volume_percents': self.volume_percents,
            'modified': self.modified,
            'facebook_scrobbling_enabled': self.facebook_scrobbling_enabled,
            'add_new_track_on_playlist_top': self.add_new_track_on_playlist_top,
            'user_music_visibility': self.user_music_visibility,
            'user_social_visibility': self.user_social_visibility,
            'rbt_disabled': self.rbt_disabled,
            'theme': self.theme,
            'promos_disabled': self.promos_disabled,
            'auto_play_radio': self.auto_play_radio,
            'sync_queue_enabled': self.sync_queue_enabled,
            'ads_disabled': self.ads_disabled,
            'disk_enabled': self.disk_enabled,
            'show_disk_tracks_in_library': self.show_disk_tracks_in_library,
        }
        user_settings = UserSettings.de_json(json_dict, client)

        assert user_settings.uid == self.uid
        assert user_settings.last_fm_scrobbling_enabled == self.last_fm_scrobbling_enabled
        assert user_settings.shuffle_enabled == self.shuffle_enabled
        assert user_settings.volume_percents == self.volume_percents
        assert user_settings.modified == self.modified
        assert user_settings.facebook_scrobbling_enabled == self.facebook_scrobbling_enabled
        assert user_settings.add_new_track_on_playlist_top == self.add_new_track_on_playlist_top
        assert user_settings.user_music_visibility == self.user_music_visibility
        assert user_settings.user_social_visibility == self.user_social_visibility
        assert user_settings.rbt_disabled == self.rbt_disabled
        assert user_settings.theme == self.theme
        assert user_settings.promos_disabled == self.promos_disabled
        assert user_settings.auto_play_radio == self.auto_play_radio
        assert user_settings.sync_queue_enabled == self.sync_queue_enabled
        assert user_settings.ads_disabled == self.ads_disabled
        assert user_settings.disk_enabled == self.disk_enabled
        assert user_settings.show_disk_tracks_in_library == self.show_disk_tracks_in_library

    def test_equality(self):
        a = UserSettings(
            self.uid,
            self.last_fm_scrobbling_enabled,
            self.shuffle_enabled,
            self.volume_percents,
            self.modified,
            self.facebook_scrobbling_enabled,
            self.add_new_track_on_playlist_top,
            self.user_music_visibility,
            self.user_social_visibility,
            self.rbt_disabled,
            self.theme,
            self.promos_disabled,
            self.auto_play_radio,
            self.sync_queue_enabled,
            self.ads_disabled,
            self.disk_enabled,
            self.show_disk_tracks_in_library,
        )
        b = UserSettings(
            self.uid,
            self.last_fm_scrobbling_enabled,
            self.shuffle_enabled,
            self.volume_percents,
            self.modified,
            self.facebook_scrobbling_enabled,
            self.add_new_track_on_playlist_top,
            'private',
            self.user_social_visibility,
            self.rbt_disabled,
            'white',
            self.promos_disabled,
            self.auto_play_radio,
            self.sync_queue_enabled,
            self.ads_disabled,
            True,
            self.show_disk_tracks_in_library,
        )
        c = UserSettings(
            self.uid,
            self.last_fm_scrobbling_enabled,
            self.shuffle_enabled,
            self.volume_percents,
            self.modified,
            self.facebook_scrobbling_enabled,
            self.add_new_track_on_playlist_top,
            self.user_music_visibility,
            self.user_social_visibility,
            self.rbt_disabled,
            self.theme,
            self.promos_disabled,
            self.auto_play_radio,
            self.sync_queue_enabled,
            self.ads_disabled,
            self.disk_enabled,
            self.show_disk_tracks_in_library,
        )

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == c
        assert hash(a) == hash(c)
