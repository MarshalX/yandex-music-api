import logging
from datetime import datetime

from yandex_music import YandexMusicObject, Status, Settings, PermissionAlerts, Experiments, Artist, Album, Playlist, \
    TracksLikes, Track, AlbumsLikes, ArtistsLikes, PlaylistsLikes, Feed, PromoCodeStatus, DownloadInfo, Search, \
    Suggestions, Landing
from yandex_music.utils.request import Request
from yandex_music.utils.difference import Difference
from yandex_music.exceptions import InvalidToken


CLIENT_ID = '23cabbbdc6cd418abb4b39c32c41195d'
CLIENT_SECRET = '53bc75238f0c4d08a118e51fe9203300'


class Client(YandexMusicObject):
    def __init__(self, username, password, token=None, base_url=None, oauth_url=None, request=None):
        self.logger = logging.getLogger(__name__)
        self.token = token

        if base_url is None:
            base_url = 'https://api.music.yandex.net'
        if oauth_url is None:
            oauth_url = 'https://oauth.yandex.ru'

        self.base_url = base_url
        self.oauth_url = oauth_url

        self._request = request or Request(self)

        if self.token is None:
            self.token = self._generate_token_by_username_and_password(username, password)
            self.request.set_authorization(self.token)

        self.account = self.account_status().account

    @classmethod
    def from_token(cls, token):
        return cls(username=None, password=None, token=token)

    def _generate_token_by_username_and_password(self, username, password, grant_type='password',
                                                 timeout=None, *args, **kwargs):
        url = f'{self.oauth_url}/token'

        data = {
            'grant_type': grant_type,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'username': username,
            'password': password
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return result.get('access_token')

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

        return Status.de_json(result, self)

    def settings(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/settings'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Settings.de_json(result, self)

    def permission_alerts(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/permission-alerts'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return PermissionAlerts.de_json(result, self)

    def account_experiments(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/account/experiments'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Experiments.de_json(result, self)

    def consume_promo_code(self, code: str, language='en', timeout=None, *args, **kwargs):
        url = f'{self.base_url}/account/consume-promo-code'

        result = self._request.post(url, {'code': code, 'language': language}, timeout=timeout, *args, **kwargs)

        return PromoCodeStatus.de_json(result, self)

    def feed(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/feed'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Feed.de_json(result, self)

    def landing(self, blocks: str or list, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/landing3'

        result = self._request.get(url, {'blocks': blocks}, timeout=timeout, *args, **kwargs)

        return Landing.de_json(result, self)

    def tracks_download_info(self, track_id: str or int, get_direct_links=False, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/tracks/{track_id}/download-info'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return DownloadInfo.de_list(result, self, get_direct_links)

    def play_audio(self,
                   track_id: str or int,
                   from_,
                   album_id,
                   playlist_id,
                   from_cache=False,
                   play_id=None,
                   uid=None,
                   timestamp=None,
                   track_length_seconds=0,
                   total_played_seconds=0,
                   end_position_seconds=0,
                   client_now=None,
                   timeout=None,
                   *args, **kwargs):
        url = f'{self.base_url}/play-audio'

        data = {
            'track-id': track_id,
            'from-cache': from_cache,
            'from': from_,
            'play-id': play_id or '',
            'uid': uid or self.account.uid,
            'timestamp': timestamp or f'{datetime.now().isoformat()}Z',
            'track-length-seconds': track_length_seconds,
            'total-played-seconds': total_played_seconds,
            'end-position-seconds': end_position_seconds,
            'album-id': album_id,
            'playlist-id': playlist_id,
            'client-now': client_now or f'{datetime.now().isoformat()}Z'
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    def search(self,
               text,
               nocorrect=False,
               type='all',
               page=0,
               playlist_in_best=True,
               timeout=None,
               *args, **kwargs):
        url = f'{self.base_url}/search'

        params = {
            'text': text,
            'nocorrect': nocorrect,
            'type': type,
            'page': page,
            'playlist-in-best': playlist_in_best,
        }

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        return Search.de_json(result, self)

    def search_suggest(self, part: str, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/search/suggest'

        result = self._request.get(url, {'part': part}, timeout=timeout, *args, **kwargs)

        return Suggestions.de_json(result, self)

    def users_playlists(self, kind: str or int, user_id: str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_create(self, title: str, visibility: str = 'public', user_id: str = None,
                               timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/create'

        data = {
            'title': title,
            'visibility': visibility
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_delete(self, kind: str or int, user_id: str = None,
                               timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/delete'

        result = self._request.post(url, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    def users_playlists_name(self, kind: str or int, name: str, user_id: str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/name'

        result = self._request.post(url, {'value': name}, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_change(self, kind: str or int, diff: str, revision: int = 1, user_id: str = None,
                               timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/change'

        data = {
            'kind': kind,
            'revision': revision,
            'diff': diff
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_insert_track(self, kind: str or int, track_id, album_id, at: int = 0, revision: int = 1,
                                     user_id: str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        diff = Difference().add_insert(at, {'id': track_id, 'album_id': album_id})

        return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

    def users_playlists_delete_track(self, kind: str or int, from_: int, to: int, revision: int = 1,
                                     user_id: str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        diff = Difference().add_delete(from_, to)

        return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

    def _add_like(self, object_type: str, ids: str or int or list, remove: bool = False, user_id: str or int = None,
                  timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s/{action}'

        result = self._request.post(url, {f'{object_type}-ids': ids}, timeout=timeout, *args, **kwargs)

        if object_type == 'track':
            return 'revision' in result

        return result == 'ok'

    def users_likes_tracks_add(self, track_ids: str or list, user_id: str or int = None,
                               timeout=None, *args, **kwargs):
        return self._add_like('track', track_ids, user_id, timeout, *args, **kwargs)

    def users_likes_tracks_remove(self, track_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._add_like('track', track_ids, True, user_id, timeout, *args, **kwargs)

    def users_likes_artists_add(self, artist_ids: str or int or list, user_id: str or int = None,
                                timeout=None, *args, **kwargs):
        return self._add_like('artist', artist_ids, user_id, timeout, *args, **kwargs)

    def users_likes_artists_remove(self, artist_ids: str or list, user_id: str or int = None,
                                   timeout=None, *args, **kwargs):
        return self._add_like('artist', artist_ids, True, user_id, timeout, *args, **kwargs)

    def users_likes_playlists_add(self, playlist_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._add_like('playlist', playlist_ids, user_id, timeout, *args, **kwargs)

    def users_likes_playlists_remove(self, playlist_ids: str or list, user_id: str or int = None,
                                     timeout=None, *args, **kwargs):
        return self._add_like('playlist', playlist_ids, True, user_id, timeout, *args, **kwargs)

    def users_likes_albums_add(self, album_ids: str or list, user_id: str or int = None,
                               timeout=None, *args, **kwargs):
        return self._add_like('album', album_ids, user_id, timeout, *args, **kwargs)

    def users_likes_albums_remove(self, album_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._add_like('album', album_ids, True, user_id, timeout, *args, **kwargs)

    def _get_list(self, object_type: str, ids: list or int or str, params=None, timeout=None, *args, **kwargs):
        de_list = {
            'artist': Artist.de_list,
            'album': Album.de_list,
            'track': Track.de_list,
            'playlist': Playlist.de_list,
        }

        if params is None:
            params = {}
        params.update({f'{object_type}-ids': ids})

        url = f'{self.base_url}/{object_type}s' + ('/list' if object_type == 'playlist' else '')

        result = self._request.post(url, params, timeout=timeout, *args, **kwargs)

        return de_list.get(object_type)(result, self)

    def artists(self, artist_ids: list or int or str, timeout=None, *args, **kwargs):
        return self._get_list('artist', artist_ids, timeout, *args, **kwargs)

    def albums(self, album_ids: list or int or str, timeout=None, *args, **kwargs):
        return self._get_list('album', album_ids, timeout, *args, **kwargs)

    def tracks(self, track_ids: int or str, with_positions=True, timeout=None, *args, **kwargs):
        return self._get_list('track', track_ids, {'with-positions': with_positions}, timeout, *args, **kwargs)

    def playlists_list(self, playlist_ids: list or int or str, timeout=None, *args, **kwargs):
        return self._get_list('playlist', playlist_ids, timeout, *args, **kwargs)

    def users_playlists_list(self, user_id: int or str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/list'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Playlist.de_list(result, self)

    def _get_likes(self, object_type, user_id: int or str = None, params=None, timeout=None, *args, **kwargs):
        de_list = {
            'artist': ArtistsLikes.de_list,
            'album': AlbumsLikes.de_list,
            'playlist': PlaylistsLikes.de_list,
        }

        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s'

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        if object_type == 'track':
            return TracksLikes.de_json(result.get('library'), self)

        return de_list.get(object_type)(result, self)

    def users_likes_tracks(self, user_id: int or str = None, if_modified_since_revision=0, timeout=None,
                           *args, **kwargs):
        return self._get_likes('track', user_id, {'if-modified-since-revision': if_modified_since_revision}, timeout,
                               *args, **kwargs)

    def users_likes_albums(self, user_id: int or str = None, rich=True, timeout=None, *args, **kwargs):
        return self._get_likes('album', user_id, {'rich': rich}, timeout, *args, **kwargs)

    def users_likes_artists(self, user_id: int or str = None, with_timestamps=True, timeout=None, *args, **kwargs):
        return self._get_likes('artist', user_id, {'with-timestamps': with_timestamps}, timeout, *args, **kwargs)

    def users_likes_playlists(self, user_id: int or str = None, timeout=None, *args, **kwargs):
        return self._get_likes('playlist', user_id, timeout=timeout, *args, **kwargs)
