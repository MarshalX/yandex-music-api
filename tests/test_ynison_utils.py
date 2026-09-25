import pytest

pytest.importorskip('betterproto')
pytest.importorskip('websockets')

from yandex_music.ynison import utils
from yandex_music.ynison.models import ynison_state

from .ynison_fake_server import PLAYER_DEVICE_ID, make_playing_status, make_queue, make_state


class TestGetCurrentPlayable:
    def test_current(self):
        state = make_state(queue=make_queue(size=3, current=1))

        playable = utils.get_current_playable(state)

        assert playable is not None
        assert playable.playable_id == '1001'

    @pytest.mark.parametrize(('size', 'current'), [(3, -1), (3, 3), (3, 100), (0, 0), (0, -1)])
    def test_out_of_range(self, size, current):
        assert utils.get_current_playable(make_state(queue=make_queue(size=size, current=current))) is None

    def test_empty_state(self):
        assert utils.get_current_playable(ynison_state.PutYnisonStateResponse()) is None


class TestGetActiveDevice:
    def test_found(self):
        device = utils.get_active_device(make_state(active=True))

        assert device is not None
        assert device.info.device_id == PLAYER_DEVICE_ID

    def test_no_active(self):
        assert utils.get_active_device(make_state(active=False)) is None

    def test_active_id_not_in_devices(self):
        state = make_state(active=True)
        state.active_device_id_optional = 'unknowndevic'

        assert utils.get_active_device(state) is None

    def test_empty_active_id(self):
        state = make_state(active=True)
        state.active_device_id_optional = ''

        assert utils.get_active_device(state) is None


class TestPlaybackOrder:
    def test_linear(self):
        assert utils.get_playback_order(make_queue(size=4)) == [0, 1, 2, 3]

    def test_shuffle(self):
        assert utils.get_playback_order(make_queue(size=3, shuffle=[1, 2, 0])) == [1, 2, 0]

    def test_empty_shuffle_is_linear(self):
        assert utils.get_playback_order(make_queue(size=3, shuffle=[])) == [0, 1, 2]

    def test_shuffle_length_mismatch_is_linear(self):
        assert utils.get_playback_order(make_queue(size=3, shuffle=[1, 0])) == [0, 1, 2]

    def test_shuffle_none(self):
        queue = make_queue(size=2)
        queue.shuffle_optional = None

        assert utils.get_playback_order(queue) == [0, 1]

    def test_empty_queue(self):
        assert utils.get_playback_order(make_queue(size=0)) == []


class TestNeighbourIndex:
    def test_linear(self):
        queue = make_queue(size=3, current=1)

        assert utils.get_neighbour_index(queue, 1) == 2
        assert utils.get_neighbour_index(queue, -1) == 0
        assert utils.get_neighbour_index(queue, 0) == 1

    def test_shuffle(self):
        queue = make_queue(size=4, current=3, shuffle=[2, 3, 0, 1])

        assert utils.get_neighbour_index(queue, 1) == 0
        assert utils.get_neighbour_index(queue, -1) == 2
        assert utils.get_neighbour_index(queue, 2) == 1
        assert utils.get_neighbour_index(queue, 3) is None

    def test_boundaries(self):
        assert utils.get_neighbour_index(make_queue(size=3, current=2), 1) is None
        assert utils.get_neighbour_index(make_queue(size=3, current=0), -1) is None

    def test_current_not_in_order(self):
        assert utils.get_neighbour_index(make_queue(size=3, current=-1), 1) is None
        assert utils.get_neighbour_index(make_queue(size=3, current=7), -1) is None
        assert utils.get_neighbour_index(make_queue(size=0, current=0), 1) is None


class TestCurrentProgress:
    def test_playing(self):
        status = make_playing_status(progress_ms=1000, duration_ms=100000, paused=False, timestamp_ms=10000)

        assert utils.get_current_progress_ms(status, now_ms=12500) == 3500

    def test_playback_speed(self):
        status = make_playing_status(
            progress_ms=1000, duration_ms=100000, paused=False, playback_speed=2.0, timestamp_ms=10000
        )

        assert utils.get_current_progress_ms(status, now_ms=12000) == 5000

    def test_zero_speed_treated_as_normal(self):
        status = make_playing_status(progress_ms=0, paused=False, playback_speed=0, timestamp_ms=10000)

        assert utils.get_current_progress_ms(status, now_ms=11000) == 1000

    def test_paused(self):
        status = make_playing_status(progress_ms=1000, paused=True, timestamp_ms=10000)

        assert utils.get_current_progress_ms(status, now_ms=99999) == 1000

    def test_clamped_to_duration(self):
        status = make_playing_status(progress_ms=1000, duration_ms=5000, paused=False, timestamp_ms=10000)

        assert utils.get_current_progress_ms(status, now_ms=100000) == 5000

    def test_unknown_duration_not_clamped(self):
        status = make_playing_status(progress_ms=1000, duration_ms=0, paused=False, timestamp_ms=10000)

        assert utils.get_current_progress_ms(status, now_ms=20000) == 11000

    def test_clock_skew_does_not_go_back(self):
        status = make_playing_status(progress_ms=1000, paused=False, timestamp_ms=10000)

        assert utils.get_current_progress_ms(status, now_ms=5000) == 1000

    def test_no_timestamp(self):
        status = make_playing_status(progress_ms=1000, paused=False, timestamp_ms=0)

        assert utils.get_current_progress_ms(status, now_ms=99999) == 1000

    def test_no_version(self):
        status = make_playing_status(progress_ms=1000, paused=False, timestamp_ms=10000)
        status.version = None

        assert utils.get_current_progress_ms(status, now_ms=99999) == 1000

    def test_default_now(self):
        status = make_playing_status(progress_ms=0, duration_ms=0, paused=False, timestamp_ms=1)

        assert utils.get_current_progress_ms(status) > 0
