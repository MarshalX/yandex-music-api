from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Artist, Label, TrackPosition, Track

from yandex_music import YandexMusicObject


class Album(YandexMusicObject):
    def __init__(self,
                 id_: int,
                 title: str,
                 track_count: int,
                 artists: List['Artist'],
                 labels: List['Label'],
                 available: bool,
                 available_for_premium_users: bool,
                 cover_uri: Optional[str] = None,
                 content_warning=None,
                 original_release_year=None,
                 genre: Optional[str] = None,
                 og_image: Optional[str] = None,
                 buy: Optional[list] = None,
                 recent: Optional[bool] = None,
                 very_important: Optional[bool] = None,
                 available_for_mobile: Optional[bool] = None,
                 available_partially: Optional[bool] = None,
                 bests: Optional[List[int]] = None,
                 prerolls: Optional[list] = None,
                 volumes: List['Track'] = None,
                 year: Optional[int] = None,
                 release_date: Optional[str] = None,
                 type_: Optional[str] = None,
                 track_position: Optional['TrackPosition'] = None,
                 regions=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
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
        self.type = type_
        self.track_position = track_position
        self.regions = regions
        self.original_release_year = original_release_year
        self.content_warning = content_warning

        self.client = client
        self._id_attrs = (self.id, self.title, self.track_count, self.artists, self.labels,
                          self.available_for_premium_users, self.available)

    def with_tracks(self, *args, **kwargs) -> Optional['Album']:
        """Сокращение для::

            client.albums_with_tracks(album.id, *args, **kwargs)
        """

        return self.client.albums_with_tracks(self.id, *args, **kwargs)

    def download_cover(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """

        self.client.request.download(f'https://{self.cover_uri.replace("%%", size)}', filename)

    def download_og_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Предпочтительнее использовать self.download_cover().

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """

        self.client.request.download(f'https://{self.og_image.replace("%%", size)}', filename)

    def like(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_albums_add(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_add(self.id, self.client.me.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs) -> bool:
        """Сокращение для::

            client.users_likes_albums_remove(album.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_albums_remove(self.id, self.client.me.account.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Album']:
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
    def de_list(cls, data: dict, client: 'Client') -> List['Album']:
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
