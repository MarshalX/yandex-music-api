from typing import Dict

from yandex_music import Artist, ArtistAbout, ArtistLink, Client, Cover, JSONType, Stats


class TestArtistAbout:
    description = 'Fake artist bio text'
    artist_type = 'artist'

    def test_expected_value(
        self, about_artist: ArtistAbout, artist: Artist, stats: Stats, artist_link: ArtistLink, cover: Cover
    ) -> None:
        assert about_artist.artist == artist
        assert about_artist.stats == stats
        assert about_artist.description == self.description
        assert about_artist.links == [artist_link]
        assert about_artist.covers == [cover]
        assert about_artist.artist_type == self.artist_type

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistAbout.de_json({}, client) is None

    def test_de_json_all(
        self, client: Client, artist: Artist, stats: Stats, artist_link: ArtistLink, cover: Cover
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'stats': stats.to_dict(),
            'description': self.description,
            'links': [artist_link.to_dict()],
            'covers': [cover.to_dict()],
            'artistType': self.artist_type,
        }
        obj = ArtistAbout.de_json(json_dict, client)
        assert obj is not None

        assert obj.artist == artist
        assert obj.stats == stats
        assert obj.description == self.description
        assert obj.artist_type == self.artist_type

    def test_equality(self, artist: Artist) -> None:
        a = ArtistAbout(artist=artist)
        b = ArtistAbout(artist=None)
        c = ArtistAbout(artist=artist)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
