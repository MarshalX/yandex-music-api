from yandex_music import YandexMusicObject


class Track(YandexMusicObject):
    def __init__(self,
                 id,
                 title,
                 available,
                 artists,
                 albums,
                 available_for_premium_users=None,
                 lyrics_available=None,
                 real_id=None,
                 og_image=None,
                 type=None,
                 cover_uri=None,
                 major=None,
                 duration_ms=None,
                 storage_dir=None,
                 file_size=None,
                 normalization=None,
                 error=None,
                 regions=None,
                 available_as_rbt=None,
                 content_warning=None,
                 explicit=None,
                 preview_duration_ms=None,
                 available_full_without_permission=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.title = title
        self.available = available
        self.artists = artists
        self.albums = albums

        self.available_for_premium_users = available_for_premium_users
        self.lyrics_available = lyrics_available
        self.real_id = real_id
        self.og_image = og_image
        self.type = type
        self.cover_uri = cover_uri
        self.major = major
        self.duration_ms = duration_ms
        self.storage_dir = storage_dir
        self.file_size = file_size
        self.normalization = normalization
        self.error = error
        self.regions = regions
        self.available_as_rbt = available_as_rbt
        self.content_warning = content_warning
        self.explicit = explicit
        self.preview_duration_ms = preview_duration_ms
        self.available_full_without_permission = available_full_without_permission

        self.download_info = None

        self.client = client
        self._id_attrs = (self.id, self.title, self.available, self.artists, self.albums)

    def get_download_info(self, get_direct_links=False):
        self.download_info = self.client.tracks_download_info(self.track_id, get_direct_links)

        return self.download_info

    def get_supplement(self, *args, **kwargs):
        """Сокращение для::

            client.track_supplement(track.id, *args, **kwargs)
        """
        return self.client.track_supplement(self.id, *args, **kwargs)

    def download_cover(self, filename, size='200x200'):
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """

        self.client.request.download(f'https://{self.cover_uri.replace("%%", size)}', filename)

    def download_og_image(self, filename, size='200x200'):
        """Загрузка обложки.

        Предпочтительнее использовать self.download_cover().

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """

        self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

    def download(self, filename, codec='mp3', bitrate_in_kbps=192):
        if self.download_info is None:
            self.get_download_info()

        for info in self.download_info:
            if info.codec == codec and info.bitrate_in_kbps == bitrate_in_kbps:
                info.download(filename)

    def like(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_tracks_add(track.id, user.id, *args, **kwargs)
        """
        return self.client.users_likes_tracks_add(self.track_id, self.client.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_tracks_remove(track.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_tracks_remove(self.track_id, self.client.account.uid, *args, **kwargs)

    @property
    def track_id(self):
        return f'{self.id}'

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Track, cls).de_json(data, client)
        from yandex_music import Normalization, Major, Album, Artist
        data['albums'] = Album.de_list(data.get('albums'), client)
        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['normalization'] = Normalization.de_json(data.get('normalization'), client)
        data['major'] = Major.de_json(data.get('major'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_download_info`
    getDownloadInfo = get_download_info
    #: Псевдоним для :attr:`get_supplement`
    getSupplement = get_supplement
    #: Псевдоним для :attr:`download_cover`
    downloadCover = download_cover
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
    #: Псевдоним для :attr:`track_id`
    trackId = track_id
