from yandex_music import YandexMusicObject


class Playlist(YandexMusicObject):
    def __init__(self,
                 owner,
                 cover,
                 made_for,
                 play_counter,
                 playlist_absence,
                 uid=None,
                 kind=None,
                 title=None,
                 track_count=None,
                 tags=None,
                 revision=None,
                 snapshot=None,
                 visibility=None,
                 collective=None,
                 created=None,
                 modified=None,
                 available=None,
                 is_banner=None,
                 is_premiere=None,
                 duration_ms=None,
                 og_image=None,
                 tracks=None,
                 prerolls=None,
                 likes_count=None,
                 generated_playlist_type=None,
                 animated_cover_uri=None,
                 ever_played=None,
                 description=None,
                 description_formatted=None,
                 is_for_from=None,
                 regions=None,
                 client=None,
                 **kwargs):
        self.owner = owner
        self.cover = cover
        self.made_for = made_for
        self.play_counter = play_counter
        self.playlist_absence = playlist_absence

        self.uid = uid
        self.kind = kind
        self.title = title
        self.track_count = track_count
        self.revision = revision
        self.snapshot = snapshot
        self.visibility = visibility
        self.collective = collective
        self.created = created
        self.modified = modified
        self.available = available
        self.is_banner = is_banner
        self.is_premiere = is_premiere
        self.duration_ms = duration_ms
        self.og_image = og_image
        self.tracks = tracks
        self.prerolls = prerolls
        self.likes_count = likes_count
        self.animated_cover_uri = animated_cover_uri
        self.description = description
        self.description_formatted = description_formatted
        self.ever_played = ever_played
        self.generated_playlist_type = generated_playlist_type
        self.is_for_from = is_for_from
        self.regions = regions
        self.tags = tags

        self.client = client
        self._id_attrs = (self.uid, self.kind, self.title, self.playlist_absence)

    @property
    def is_mine(self):
        return self.owner.uid == self.client.account.uid

    @property
    def playlist_id(self):
        return f'{self.owner.uid}:{self.kind}'

    def download_animated_cover(self, filename, size='200x200'):
        """Загрузка анимированной обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением (GIF).
            size (:obj:`str`, optional): Размер анимированной обложки.
        """

        self.client.request.download(f'https://{self.animated_cover_uri.replace("%%", size)}', filename)

    def download_og_image(self, filename, size='200x200'):
        """Загрузка обложки.

        Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """

        self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

    def rename(self, name):
        client, kind = self.client, self.kind

        self.__dict__.clear()
        self.__dict__.update(client.users_playlists_name(kind, name).__dict__)

    def like(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_playlists_add(playlist.uid, user.id *args, **kwargs)
        """
        return self.client.users_likes_playlists_add(self.uid, self.client.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_playlists_remove(playlist.uid, user.id *args, **kwargs)
        """
        return self.client.users_likes_playlists_remove(self.uid, self.client.account.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Playlist, cls).de_json(data, client)
        from yandex_music import User, MadeFor, Cover, PlayCounter, TrackShort, PlaylistAbsence
        data['owner'] = User.de_json(data.get('owner'), client)
        data['cover'] = Cover.de_json(data.get('cover'), client)
        data['made_for'] = MadeFor.de_json(data.get('made_for'), client)
        data['tracks'] = TrackShort.de_list(data.get('tracks'), client)
        data['play_counter'] = PlayCounter.de_json(data.get('play_counter'), client)

        data['playlist_absence'] = PlaylistAbsence.de_json(data.get('playlist_absence'), client)    # на случай фикса
        if data.get('playlist_absense'):    # очепятка яндуха
            data['playlist_absence'] = PlaylistAbsence.de_json(data.get('playlist_absense'), client)
            data.pop('playlist_absense')

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        playlists = list()
        for playlist in data:
            playlists.append(cls.de_json(playlist, client))

        return playlists

    # camelCase псевдонимы

    #: Псевдоним для :attr:`is_mine`
    isMine = is_mine
    #: Псевдоним для :attr:`playlist_id`
    playlistId = playlist_id
    #: Псевдоним для :attr:`download_animated_cover`
    downloadAnimatedCover = download_animated_cover
    #: Псевдоним для :attr:`download_og_image`
    downloadOgImage = download_og_image
