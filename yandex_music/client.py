import logging

from yandex_music import YandexMusicObject, Status, Settings, PermissionAlerts, Experiments, Artist, Album, Playlist, \
    TracksLikes, Track, AlbumsLikes, ArtistsLikes
from yandex_music.utils.request import Request
from yandex_music.error import InvalidToken


class Client(YandexMusicObject):
    def __init__(self, token, base_url=None, request=None):
        self.token = token
        self._request = request or Request(token)
        self.logger = logging.getLogger(__name__)

        if base_url is None:
            base_url = 'https://api.music.yandex.net'

        self.base_url = base_url

        self.account = self.account_status().account

    @staticmethod
    def _validate_token(token):
        if any(x.isspace() for x in token):
            raise InvalidToken()

        if len(token) != 39:
            raise InvalidToken()

        return token

    @property
    def request(self):
        return self._request

    def account_status(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/account/status'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        status = Status.de_json(result, self)

        return status

    def settings(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/settings'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        settings = Settings.de_json(result, self)

        return settings

    def permission_alerts(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/permission-alerts'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        permission_alerts = PermissionAlerts.de_json(result, self)

        return permission_alerts

    def account_experiments(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/account/experiments'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        experiments = Experiments.de_json(result, self)

        return experiments

    def artists(self, artist_ids: list or int or str, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/artists'

        result = self._request.post(url, {'artist-ids': artist_ids}, timeout=timeout, *args, **kwargs)

        artists = Artist.de_list(result, self)

        return artists

    def albums(self, album_ids: list or int or str, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/albums'

        result = self._request.post(url, {'album-ids': album_ids}, timeout=timeout, *args, **kwargs)

        albums = Album.de_list(result, self)

        return albums

    def tracks(self, track_ids: int or str, with_positions=True, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/tracks'

        result = self._request.post(url, {'track-ids': track_ids, 'with-positions': with_positions},
                                    timeout=timeout, *args, **kwargs)

        tracks = Track.de_list(result, self)

        return tracks

    def playlists_list(self, playlist_ids: list or int or str, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/playlists/list'

        result = self._request.post(url, {'playlistIds': playlist_ids}, timeout=timeout, *args, **kwargs)

        playlists = Playlist.de_list(result, self)

        return playlists

    def users_playlists_list(self, user_id: int or str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/list'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        playlists = Playlist.de_list(result, self)

        return playlists

    def users_likes_tracks(self, user_id: int or str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/likes/tracks'

        result = self._request.get(url, timeout=timeout, *args, **kwargs).get('library')

        tracks_likes = TracksLikes.de_json(result, self)

        return tracks_likes

    def users_likes_albums(self, user_id: int or str = None, rich=True, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/likes/albums?rich={rich}'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        albums_likes = AlbumsLikes.de_list(result, self)

        return albums_likes

    def users_likes_artists(self, user_id: int or str = None, with_timestamps=True, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/likes/artists?with-timestamps={with_timestamps}'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        artists_likes = ArtistsLikes.de_list(result, self)

        return artists_likes
