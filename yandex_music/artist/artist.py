from yandex_music import YandexMusicObject


class Artist(YandexMusicObject):
    def __init__(self,
                 id,
                 name,
                 cover,
                 various=None,
                 composer=None,
                 genres=None,
                 op_image=None,
                 no_pictures_from_search=None,
                 counts=None,
                 available=None,
                 ratings=None,
                 links=None,
                 tickets_available=None,
                 likes_count=None,
                 popular_tracks=None,
                 regions=None,
                 decomposed=None,
                 full_names=None,
                 description=None,
                 countries=None,
                 en_wikipedia_link=None,
                 db_aliases=None,
                 aliases=None,
                 init_date=None,
                 end_date=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.name = name
        self.cover = cover

        self.various = various
        self.composer = composer
        self.genres = genres
        self.op_image = op_image
        self.no_pictures_from_search = no_pictures_from_search
        self.counts = counts
        self.available = available
        self.ratings = ratings
        self.links = links
        self.tickets_available = tickets_available
        self.regions = regions
        self.decomposed = decomposed
        self.popular_tracks = popular_tracks
        self.likes_count = likes_count
        self.full_names = full_names
        self.description = description
        self.countries = countries
        self.en_wikipedia_link = en_wikipedia_link
        self.db_aliases = db_aliases
        self.aliases = aliases

        # Может прийти конкретная дата или просто год
        self.init_date = init_date
        self.end_date = end_date

        self.client = client
        self._id_attrs = (self.id, self.name, self.cover)

    def download_op_image(self, filename, size='200x200'):
        """Загрузка обложки.

        Используйте это только когда нет self.cover!

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """

        self.client.request.download(f'https://{self.op_image.replace("%%", size)}', filename)

    def like(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_artists_add(artist.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_artists_add(self.id, self.client.account.uid, *args, **kwargs)

    def dislike(self, *args, **kwargs):
        """Сокращение для::

            client.users_likes_artists_remove(artist.id, user.id *args, **kwargs)
        """
        return self.client.users_likes_artists_remove(self.id, self.client.account.uid, *args, **kwargs)

    def get_tracks(self, page=0, page_size=20, *args, **kwargs):
        """Сокращение для::

            client.artists_tracks(artist.id, page, page_size, *args, **kwargs)
        """
        return self.client.artists_tracks(self.id, page, page_size, *args, **kwargs)

    def get_albums(self, page=0, page_size=20, sort_by='year', *args, **kwargs):
        """Сокращение для::

            client.artists_direct_albums(artist.id, page, page_size, sort_by, *args, **kwargs)
        """
        return self.client.artists_direct_albums(self.id, page, page_size, sort_by, *args, **kwargs)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Artist, cls).de_json(data, client)
        from yandex_music import Cover, Ratings, Counts, Link, Track, Description
        data['cover'] = Cover.de_json(data.get('cover'), client)
        data['ratings'] = Ratings.de_json(data.get('ratings'), client)
        data['counts'] = Counts.de_json(data.get('counts'), client)
        data['links'] = Link.de_list(data.get('links'), client)
        data['popular_tracks'] = Track.de_list(data.get('popular_tracks'), client)
        data['description'] = Description.de_json(data.get('description'), client)
        # TODO add "decomposed" deserialization

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        artists = list()
        for artist in data:
            artists.append(cls.de_json(artist, client))

        return artists

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_op_image`
    downloadOpImage = download_op_image
    #: Псевдоним для :attr:`get_tracks`
    getTracks = get_tracks
    #: Псевдоним для :attr:`get_albums`
    getAlbums = get_albums
