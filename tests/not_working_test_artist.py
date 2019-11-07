from yandex_music import Artist


class TestArtist:
    name = None
    various = None
    composer = None
    genres = None
    op_image = None
    no_pictures_from_search = None
    available = None
    tickets_available = None
    likes_count = None
    regions = None
    decomposed = None
    full_names = None
    countries = None
    en_wikipedia_link = None
    db_aliases = None
    aliases = None
    init_date = None
    end_date = None

    def test_expected_values(self, artist, id, cover, counts, ratings, links, popular_tracks, description):
        assert artist.id == id
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
        assert artist.links == links
        assert artist.tickets_available == self.tickets_available
        assert artist.likes_count == self.likes_count
        assert artist.popular_tracks == popular_tracks
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

    def test_de_json_required(self, client, id, cover):
        json_dict = {'id': id, 'name': self.name, 'various': self.various, 'composer': self.composer, 'cover': cover}
        artist = Artist.de_json(json_dict, client)

        assert artist.id == id
        assert artist.name == self.name
        assert artist.various == self.various
        assert artist.composer == self.composer
        assert artist.cover == cover

    def test_de_json_all(self, client, id, cover, counts, ratings, links, popular_tracks, description):
        json_dict = {'id': id, 'name': self.name, 'various': self.various, 'composer': self.composer, 'cover': cover,
                     'genres': self.genres, 'op_image': self.op_image,
                     'no_pictures_from_search': self.no_pictures_from_search, 'counts': counts,
                     'available': self.available, 'ratings': ratings, 'links': links,
                     'tickets_available': self.tickets_available, 'likes_count': self.likes_count,
                     'popular_tracks': popular_tracks, 'regions': self.regions, 'decomposed': self.decomposed,
                     'full_names': self.full_names, 'description': description, 'countries': self.countries,
                     'en_wikipedia_link': self.en_wikipedia_link, 'db_aliases': self.db_aliases,
                     'aliases': self.aliases, 'init_date': self.init_date, 'end_date': self.end_date}
        artist = Artist.de_json(json_dict, client)

        assert artist.id == id
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
        assert artist.links == links
        assert artist.tickets_available == self.tickets_available
        assert artist.likes_count == self.likes_count
        assert artist.popular_tracks == popular_tracks
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

    def test_equality(self):
        pass
