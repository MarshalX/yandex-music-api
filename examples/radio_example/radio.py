from random import random
from typing import Optional, Union

from yandex_music import Client, StationTracksResult, Track


class Radio:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.station_id: Optional[str] = None
        self.station_from: Optional[str] = None

        self.play_id: Optional[str] = None
        self.index: int = 0
        self.current_track: Optional[Track] = None
        self.station_tracks: Optional[StationTracksResult] = None

    def start_radio(self, station_id: str, station_from: str) -> Track:
        self.station_id = station_id
        self.station_from = station_from

        # get first 5 tracks
        self.__update_radio_batch(None)

        # setup current track
        self.current_track = self.__update_current_track()
        return self.current_track

    def play_next(self) -> Track:
        assert self.current_track is not None
        assert self.station_tracks is not None

        # send prev track finalize info
        self.__send_play_end_track(self.current_track, self.play_id)
        self.__send_play_end_radio(self.current_track, self.station_tracks.batch_id)

        # get next index
        self.index += 1
        if self.index >= len(self.station_tracks.sequence):
            # get next 5 tracks. Set index to 0
            self.__update_radio_batch(self.current_track.track_id)

        # setup next track
        self.current_track = self.__update_current_track()
        return self.current_track

    def __update_radio_batch(self, queue: Optional[Union[str, int]] = None) -> None:
        assert self.station_id is not None
        self.index = 0
        self.station_tracks = self.client.rotor_station_tracks(self.station_id, queue=queue)
        assert self.station_tracks is not None
        self.__send_start_radio(self.station_tracks.batch_id)

    def __update_current_track(self) -> Track:
        assert self.station_tracks is not None
        self.play_id = self.__generate_play_id()
        sequence_track = self.station_tracks.sequence[self.index].track
        assert sequence_track is not None
        track = self.client.tracks([sequence_track.track_id])[0]
        self.__send_play_start_track(track, self.play_id)
        self.__send_play_start_radio(track, self.station_tracks.batch_id)
        return track

    def __send_start_radio(self, batch_id: str) -> None:
        assert self.station_id is not None
        assert self.station_from is not None
        _ = self.client.rotor_station_feedback_radio_started(
            station=self.station_id, from_=self.station_from, batch_id=batch_id
        )

    def __send_play_start_track(self, track: Track, play_id: Optional[str]) -> None:
        assert track.duration_ms is not None
        total_seconds = track.duration_ms / 1000
        _ = self.client.play_audio(
            from_='desktop_win-home-playlist_of_the_day-playlist-default',
            track_id=track.id,
            album_id=self.__album_id(track),
            play_id=play_id,
            track_length_seconds=0,
            total_played_seconds=0,
            end_position_seconds=total_seconds,
        )

    def __send_play_start_radio(self, track: Track, batch_id: str) -> None:
        assert self.station_id is not None
        _ = self.client.rotor_station_feedback_track_started(
            station=self.station_id, track_id=track.id, batch_id=batch_id
        )

    def __send_play_end_track(self, track: Track, play_id: Optional[str]) -> None:
        assert track.duration_ms is not None
        # played_seconds = 5.0
        played_seconds = track.duration_ms / 1000
        total_seconds = track.duration_ms / 1000
        _ = self.client.play_audio(
            from_='desktop_win-home-playlist_of_the_day-playlist-default',
            track_id=track.id,
            album_id=self.__album_id(track),
            play_id=play_id,
            track_length_seconds=int(total_seconds),
            total_played_seconds=played_seconds,
            end_position_seconds=total_seconds,
        )

    def __send_play_end_radio(self, track: Track, batch_id: str) -> None:
        assert self.station_id is not None
        assert track.duration_ms is not None
        played_seconds = track.duration_ms / 1000
        _ = self.client.rotor_station_feedback_track_finished(
            station=self.station_id, track_id=track.id, total_played_seconds=played_seconds, batch_id=batch_id
        )

    @staticmethod
    def __album_id(track: Track) -> int:
        album_id = track.albums[0].id
        assert album_id is not None
        return album_id

    @staticmethod
    def __generate_play_id() -> str:
        return f'{int(random() * 1000)}-{int(random() * 1000)}-{int(random() * 1000)}'
