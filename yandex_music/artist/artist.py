from yandex_music import YandexMusicObject


class Artist(YandexMusicObject):
    def __init__(self,
                 id,
                 name,
                 various,
                 composer,
                 cover,
                 genres=None,
                 op_image=None,
                 no_pictures_from_search=None,
                 counts=None,
                 available=None,
                 ratings=None,
                 links=None,
                 tickets_available=None,
                 popular_tracks=None,
                 regions=None,
                 decomposed=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.name = name
        self.various = various
        self.composer = composer
        self.cover = cover

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

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Artist, cls).de_json(data, client)
        from yandex_music import Cover, Ratings, Counts, Link, Track
        data['cover'] = Cover.de_json(data.get('cover'), client)
        data['ratings'] = Ratings.de_json(data.get('ratings'), client)
        data['counts'] = Counts.de_json(data.get('counts'), client)
        data['links'] = Link.de_list(data.get('links'), client)
        data['popular_tracks'] = Track.de_list(data.get('popular_tracks'), client)
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
