from typing import Dict, List, Optional, Union

import pytest

from yandex_music import Artist, Client, ContentRestrictions, Counts, Cover, Description, JSONType, Link, Ratings, Track
from yandex_music.exceptions import IdMissingError


class TestArtist:
    id = 10987
    error = 'not-found'
    reason = 'not-found'
    name = 'Elvis Presley'
    various = False
    composer: Optional[bool] = None
    genres: Optional[List[str]] = None
    og_image = ''
    op_image: Optional[str] = None
    no_pictures_from_search: Optional[bool] = None
    available: Optional[bool] = None
    tickets_available = False
    likes_count = 657469
    regions: Optional[List[str]] = None
    full_names: Optional[List[str]] = None
    hand_made_description = (
        'Одна из самых популярных советских рок-групп 1980-х годов. Лидером, '
        'автором практически всех текстов и музыки неизменно оставался Виктор Цой.'
    )
    countries: Optional[List[str]] = None
    en_wikipedia_link: Optional[str] = None
    db_aliases: Optional[List[str]] = None
    aliases: Optional[List[str]] = None
    init_date = '1935-01-08'
    end_date: Optional[str] = None
    ya_money_id = '4100170623944'
    disclaimers = ['foreignAgent']

    def test_expected_values(
        self,
        artist: Artist,
        cover: Cover,
        counts: Counts,
        ratings: Ratings,
        link: Link,
        track_without_artists_and_albums: Track,
        description: Description,
        artist_decomposed: List[Union[str, Artist]],
        content_restrictions: ContentRestrictions,
    ) -> None:
        assert artist.id == self.id
        assert artist.error == self.error
        assert artist.reason == self.reason
        assert artist.name == self.name
        assert artist.various == self.various
        assert artist.composer == self.composer
        assert artist.cover == cover
        assert artist.genres == self.genres
        assert artist.og_image == self.og_image
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
        assert artist.decomposed == artist_decomposed
        assert artist.full_names == self.full_names
        assert artist.hand_made_description == self.hand_made_description
        assert artist.description == description
        assert artist.countries == self.countries
        assert artist.en_wikipedia_link == self.en_wikipedia_link
        assert artist.db_aliases == self.db_aliases
        assert artist.aliases == self.aliases
        assert artist.init_date == self.init_date
        assert artist.end_date == self.end_date
        assert artist.ya_money_id == self.ya_money_id
        assert artist.disclaimers == self.disclaimers
        assert artist.content_restrictions == content_restrictions

    def test_de_json_none(self, client: Client) -> None:
        assert Artist.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Artist.de_list([], client) == []

    def test_de_json_required(self, client: Client, cover: Cover) -> None:
        # We don't have any required fields anymore,
        #   so just make sure we don't throw any errors.
        _ = Artist.de_json({}, client)

    def test_de_json_ugc(self, client: Client) -> None:
        # An example of UGC artist from #663
        artist = Artist.de_json({'name': self.name}, client)
        assert artist is not None
        assert artist.name == self.name

    def test_de_json_all(
        self,
        client: Client,
        cover: Cover,
        counts: Counts,
        ratings: Ratings,
        link: Link,
        track_without_artists: Track,
        description: Description,
        artist_decomposed: List[Union[str, Artist]],
        content_restrictions: ContentRestrictions,
    ) -> None:
        artist_decomposed_dict = [item if isinstance(item, str) else item.to_dict() for item in artist_decomposed]
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'reason': self.reason,
            'error': self.error,
            'name': self.name,
            'various': self.various,
            'composer': self.composer,
            'cover': cover.to_dict(),
            'genres': self.genres,
            'op_image': self.op_image,
            'og_image': self.og_image,
            'no_pictures_from_search': self.no_pictures_from_search,
            'counts': counts.to_dict(),
            'available': self.available,
            'ratings': ratings.to_dict(),
            'links': [link.to_dict()],
            'tickets_available': self.tickets_available,
            'likes_count': self.likes_count,
            'popular_tracks': [track_without_artists.to_dict()],
            'regions': self.regions,
            'decomposed': artist_decomposed_dict,
            'full_names': self.full_names,
            'description': description.to_dict(),
            'countries': self.countries,
            'en_wikipedia_link': self.en_wikipedia_link,
            'db_aliases': self.db_aliases,
            'aliases': self.aliases,
            'init_date': self.init_date,
            'end_date': self.end_date,
            'hand_made_description': self.hand_made_description,
            'ya_money_id': self.ya_money_id,
            'disclaimers': self.disclaimers,
            'contentRestrictions': content_restrictions.to_dict(),
        }
        artist = Artist.de_json(json_dict, client)
        assert artist is not None

        assert artist.id == self.id
        assert artist.error == self.error
        assert artist.reason == self.reason
        assert artist.name == self.name
        assert artist.various == self.various
        assert artist.composer == self.composer
        assert artist.cover == cover
        assert artist.genres == self.genres
        assert artist.og_image == self.og_image
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
        assert artist.decomposed == artist_decomposed
        assert artist.full_names == self.full_names
        assert artist.hand_made_description == self.hand_made_description
        assert artist.description == description
        assert artist.countries == self.countries
        assert artist.en_wikipedia_link == self.en_wikipedia_link
        assert artist.db_aliases == self.db_aliases
        assert artist.aliases == self.aliases
        assert artist.init_date == self.init_date
        assert artist.end_date == self.end_date
        assert artist.ya_money_id == self.ya_money_id
        assert artist.disclaimers == self.disclaimers
        assert artist.content_restrictions == content_restrictions

    def test_equality(self, cover: Cover) -> None:
        a = Artist(self.id)
        b = Artist(10)
        c = Artist(self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c

    def test_id_required(self, client: Client) -> None:
        artist = Artist.de_json({'name': self.name}, client)
        assert artist is not None

        # Make sure we throw an error if we try to access the id_required property when id is None
        with pytest.raises(IdMissingError):
            _ = artist.id_required
