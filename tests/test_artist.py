from yandex_music import Artist


class TestArtist:
    id = 10987
    error = 'not-found'
    name = 'Elvis Presley'
    various = False
    composer = None
    genres = None
    op_image = None
    no_pictures_from_search = None
    available = None
    tickets_available = False
    likes_count = 657469
    regions = None
    decomposed = None
    full_names = None
    countries = None
    en_wikipedia_link = None
    db_aliases = None
    aliases = None
    init_date = '1935-01-08'
    end_date = None

    def test_expected_values(self, artist, cover, counts, ratings, link, track_without_artists_and_albums, description):
        assert artist.id == self.id
        assert artist.error == self.error
        assert artist.name == self.name
        assert artist.various == self.various
        assert artist.composer == self.composer
        assert artist.cover == cover
        assert artist.genres == self.genres
        assert artist.op_image == self.op_image
        assert artist.no_pictures_from_search == self.no_pictures_from_search
        assert artist.counts == counts
        assert artist.available == self.available
        assert artist.ratings == ratings
        assert artist.links == [link]
        assert artist.tickets_available == self.tickets_available
        assert artist.likes_count == self.likes_count
        assert artist.popular_tracks == [track_without_artists_and_albums]
        assert artist.regions == self.regions
        assert artist.decomposed == self.decomposed
        assert artist.full_names == self.full_names
        assert artist.description == description
        assert artist.countries == self.countries
        assert artist.en_wikipedia_link == self.en_wikipedia_link
        assert artist.db_aliases == self.db_aliases
        assert artist.aliases == self.aliases
        assert artist.init_date == self.init_date
        assert artist.end_date == self.end_date

    def test_de_json_none(self, client):
        assert Artist.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Artist.de_list({}, client) == []

    def test_de_json_required(self, client, cover):
        json_dict = {'id_': self.id}
        artist = Artist.de_json(json_dict, client)

        assert artist.id == self.id

    def test_de_json_all(self, client, cover, counts, ratings, link, track_without_artists, description):
        json_dict = {'id_': self.id, 'error': self.error, 'name': self.name, 'various': self.various,
                     'composer': self.composer, 'cover': cover.to_dict(), 'genres': self.genres,
                     'op_image': self.op_image, 'no_pictures_from_search': self.no_pictures_from_search,
                     'counts': counts.to_dict(), 'available': self.available, 'ratings': ratings.to_dict(),
                     'links': [link.to_dict()], 'tickets_available': self.tickets_available,
                     'likes_count': self.likes_count, 'popular_tracks': [track_without_artists.to_dict()],
                     'regions': self.regions, 'decomposed': self.decomposed, 'full_names': self.full_names,
                     'description': description.to_dict(), 'countries': self.countries,
                     'en_wikipedia_link': self.en_wikipedia_link, 'db_aliases': self.db_aliases,
                     'aliases': self.aliases, 'init_date': self.init_date, 'end_date': self.end_date}
        artist = Artist.de_json(json_dict, client)

        assert artist.id == self.id
        assert artist.error == self.error
        assert artist.name == self.name
        assert artist.various == self.various
        assert artist.composer == self.composer
        assert artist.cover == cover
        assert artist.genres == self.genres
        assert artist.op_image == self.op_image
        assert artist.no_pictures_from_search == self.no_pictures_from_search
        assert artist.counts == counts
        assert artist.available == self.available
        assert artist.ratings == ratings
        assert artist.links == [link]
        assert artist.tickets_available == self.tickets_available
        assert artist.likes_count == self.likes_count
        assert artist.popular_tracks == [track_without_artists]
        assert artist.regions == self.regions
        assert artist.decomposed == self.decomposed
        assert artist.full_names == self.full_names
        assert artist.description == description
        assert artist.countries == self.countries
        assert artist.en_wikipedia_link == self.en_wikipedia_link
        assert artist.db_aliases == self.db_aliases
        assert artist.aliases == self.aliases
        assert artist.init_date == self.init_date
        assert artist.end_date == self.end_date

    def test_equality(self, cover):
        a = Artist(self.id)
        b = Artist(10)
        c = Artist(self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
