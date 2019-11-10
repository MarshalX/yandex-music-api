from yandex_music import YandexMusicObject


class Album(YandexMusicObject):
    def __init__(self,
                 id,
                 title,
                 track_count,
                 artists,
                 labels,
                 available,
                 available_for_premium_users,
                 cover_uri=None,
                 content_warning=None,
                 original_release_year=None,
                 genre=None,
                 og_image=None,
                 buy=None,
                 recent=None,
                 very_important=None,
                 available_for_mobile=None,
                 available_partially=None,
                 bests=None,
                 prerolls=None,
                 volumes=None,
                 year=None,
                 release_date=None,
                 type=None,
                 track_position=None,
                 regions=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.title = title
        self.track_count = track_count
        self.artists = artists
        self.labels = labels
        self.available_for_premium_users = available_for_premium_users
        self.available = available

        self.cover_uri = cover_uri
        self.genre = genre
        self.year = year
        self.release_date = release_date
        self.bests = bests
        self.prerolls = prerolls
        self.volumes = volumes
        self.og_image = og_image
        self.buy = buy
        self.recent = recent
        self.very_important = very_important
        self.available_for_mobile = available_for_mobile
        self.available_partially = available_partially
        self.type = type
        self.track_position = track_position
        self.regions = regions
        self.original_release_year = original_release_year
        self.content_warning = content_warning

        self.client = client
        self._id_attrs = (self.id, self.title, self.track_count, self.artists, self.labels,
                          self.available_for_premium_users, self.available)

    def with_tracks(self, *args, **kwargs):
        """Сокращение для::

            client.albums_with_tracks(album.id, *args, **kwargs)
        """

        return self.client.albums_with_tracks(self.id, *args, **kwargs)

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

        self.client.request.download(f'https://{self.og_image("%%", size)}', filename)

    def like(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_albums_add(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_add(self.id, self.client.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_albums_remove(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_remove(self.id, self.client.account.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Album, cls).de_json(data, client)
        from yandex_music import Artist, Label, TrackPosition, Track
        data['artists'] = Artist.de_list(data.get('artists'), client)
        data['labels'] = Label.de_list(data.get('labels'), client)
        data['track_position'] = TrackPosition.de_json(data.get('track_position'), client)
        if data.get('volumes'):
            data['volumes'] = [Track.de_list(i, client) for i in data['volumes']]

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        albums = list()
        for album in data:
            albums.append(cls.de_json(album, client))

        return albums

    # camelCase псевдонимы

    #: Псевдоним для :attr:`with_tracks`
    withTracks = with_tracks
    #: Псевдоним для :attr:`download_cover`
    downloadCover = download_cover
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
