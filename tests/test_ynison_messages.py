import re

import pytest

pytest.importorskip('betterproto')
pytest.importorskip('websockets')

from yandex_music.exceptions import YnisonQueueBoundaryError
from yandex_music.ynison import messages
from yandex_music.ynison.models import ynison_state

from .ynison_fake_server import CLIENT_DEVICE_ID, make_playing_status, make_queue


def _player_state(queue: ynison_state.PlayerQueue, paused: bool = True) -> ynison_state.PlayerState:
    return ynison_state.PlayerState(status=make_playing_status(paused=paused), player_queue=queue)


class TestChangeTrack:
    def test_linear_next_and_previous(self):
        state = _player_state(make_queue(size=3, current=1))

        next_request = messages.build_next_track_request(CLIENT_DEVICE_ID, state)
        previous_request = messages.build_previous_track_request(CLIENT_DEVICE_ID, state)

        assert next_request.update_player_state.player_state.player_queue.current_playable_index == 2
        assert previous_request.update_player_state.player_state.player_queue.current_playable_index == 0

    def test_shuffle_aware(self):
        # порядок воспроизведения: 2 -> 0 -> 1
        state = _player_state(make_queue(size=3, current=0, shuffle=[2, 0, 1]))

        next_request = messages.build_change_track_request(CLIENT_DEVICE_ID, state, delta=1)
        previous_request = messages.build_change_track_request(CLIENT_DEVICE_ID, state, delta=-1)

        assert next_request.update_player_state.player_state.player_queue.current_playable_index == 1
        assert previous_request.update_player_state.player_state.player_queue.current_playable_index == 2

    def test_shuffle_boundaries(self):
        last_in_order = _player_state(make_queue(size=3, current=1, shuffle=[2, 0, 1]))
        first_in_order = _player_state(make_queue(size=3, current=2, shuffle=[2, 0, 1]))

        with pytest.raises(YnisonQueueBoundaryError):
            messages.build_next_track_request(CLIENT_DEVICE_ID, last_in_order)
        with pytest.raises(YnisonQueueBoundaryError):
            messages.build_previous_track_request(CLIENT_DEVICE_ID, first_in_order)

        # в обратную сторону от границ двигаться можно
        assert (
            messages.build_previous_track_request(
                CLIENT_DEVICE_ID, last_in_order
            ).update_player_state.player_state.player_queue.current_playable_index
            == 0
        )

    def test_linear_boundaries(self):
        with pytest.raises(YnisonQueueBoundaryError):
            messages.build_next_track_request(CLIENT_DEVICE_ID, _player_state(make_queue(size=3, current=2)))
        with pytest.raises(YnisonQueueBoundaryError):
            messages.build_previous_track_request(CLIENT_DEVICE_ID, _player_state(make_queue(size=3, current=0)))

    def test_empty_queue(self):
        state = _player_state(make_queue(size=0, current=-1))

        with pytest.raises(YnisonQueueBoundaryError):
            messages.build_next_track_request(CLIENT_DEVICE_ID, state)
        with pytest.raises(YnisonQueueBoundaryError):
            messages.build_previous_track_request(CLIENT_DEVICE_ID, state)

    def test_request_contents(self):
        queue = make_queue(size=3, current=0)
        state = _player_state(queue, paused=False)

        request = messages.build_next_track_request(CLIENT_DEVICE_ID, state)
        new_state = request.update_player_state.player_state

        assert new_state.player_queue.entity_id == queue.entity_id
        assert new_state.player_queue.playable_list == queue.playable_list
        assert new_state.player_queue.version.device_id == CLIENT_DEVICE_ID
        assert new_state.status.progress_ms == 0
        assert new_state.status.duration_ms == 0
        assert new_state.status.paused is False
        assert new_state.status.playback_speed == 1.0
        assert new_state.status.version.device_id == CLIENT_DEVICE_ID
        assert request.rid
        # исходная очередь не изменилась
        assert queue.current_playable_index == 0


class TestSetPaused:
    def test_extrapolates_progress_when_playing(self):
        started = messages.get_timestamp() - 2000
        status = make_playing_status(
            progress_ms=1000, duration_ms=600000, paused=False, playback_speed=1.5, timestamp_ms=started
        )

        request = messages.build_set_paused_request(CLIENT_DEVICE_ID, status, paused=True)
        new_status = request.update_playing_status.playing_status

        # 1000 + 2000 * 1.5 = 4000 (плюс время выполнения теста)
        assert 4000 <= new_status.progress_ms < 4000 + 1500
        assert new_status.paused is True
        assert new_status.duration_ms == 600000
        assert new_status.playback_speed == 1.5
        assert new_status.version.device_id == CLIENT_DEVICE_ID

    def test_progress_unchanged_when_paused(self):
        status = make_playing_status(progress_ms=1234, paused=True, timestamp_ms=messages.get_timestamp() - 5000)

        request = messages.build_set_paused_request(CLIENT_DEVICE_ID, status, paused=False)
        new_status = request.update_playing_status.playing_status

        assert new_status.progress_ms == 1234
        assert new_status.paused is False

    def test_progress_clamped_to_duration(self):
        status = make_playing_status(
            progress_ms=9000, duration_ms=10000, paused=False, timestamp_ms=messages.get_timestamp() - 60000
        )

        request = messages.build_set_paused_request(CLIENT_DEVICE_ID, status, paused=True)

        assert request.update_playing_status.playing_status.progress_ms == 10000

    def test_zero_speed_defaults_to_one(self):
        status = make_playing_status(playback_speed=0)

        request = messages.build_set_paused_request(CLIENT_DEVICE_ID, status, paused=True)

        assert request.update_playing_status.playing_status.playback_speed == 1.0


class TestSetVolume:
    @pytest.mark.parametrize(('volume', 'expected'), [(1.5, 1.0), (-0.2, 0.0), (0.3, 0.3), (0, 0.0), (1, 1.0)])
    def test_clamping(self, volume, expected):
        request = messages.build_set_volume_request(CLIENT_DEVICE_ID, 'fakeplayer01', volume)

        assert request.update_volume_info.volume_info.volume == expected
        assert request.update_volume_info.device_id == 'fakeplayer01'
        assert request.update_volume_info.volume_info.version.device_id == CLIENT_DEVICE_ID


class TestDeviceId:
    def test_seeded_is_deterministic(self):
        first = messages.generate_device_id(seed='seed-a')

        assert first == messages.generate_device_id(seed='seed-a')
        assert first != messages.generate_device_id(seed='seed-b')
        assert re.fullmatch(r'[0-9a-f]{12}', first)

    def test_random(self):
        ids = {messages.generate_device_id() for _ in range(20)}

        assert len(ids) > 1
        for device_id in ids:
            assert re.fullmatch(r'[0-9a-f]{12}', device_id)


class TestFullState:
    def test_defaults(self):
        request = messages.build_full_state_request(CLIENT_DEVICE_ID)
        info = request.update_full_state.device.info

        assert info.device_id == CLIENT_DEVICE_ID
        assert info.title == messages.DEFAULT_DEVICE_TITLE
        assert info.app_name == messages.DEFAULT_APP_NAME
        assert request.update_full_state.device.capabilities.can_be_player is False
        assert request.update_full_state.device.capabilities.can_be_remote_controller is True
        assert request.update_full_state.is_currently_active is False

    def test_title_and_app_name(self):
        request = messages.build_full_state_request(CLIENT_DEVICE_ID, title='My Remote', app_name='my-app')
        info = request.update_full_state.device.info

        assert info.title == 'My Remote'
        assert info.app_name == 'my-app'
        assert '"updateFullState"' in request.to_json()

    def test_unique_rid(self):
        assert (
            messages.build_full_state_request(CLIENT_DEVICE_ID).rid
            != messages.build_full_state_request(CLIENT_DEVICE_ID).rid
        )
