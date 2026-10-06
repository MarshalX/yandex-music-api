from typing import Dict

from yandex_music import Artist, Client, JSONType, MetatagArtistEntry, Track


class TestMetatagArtistEntry:
    def test_expected_values(self, metatag_artist_entry: MetatagArtistEntry, artist: Artist, track: Track) -> None:
        assert metatag_artist_entry.artist == artist
        assert metatag_artist_entry.popular_tracks == [track]

    def test_de_json_none(self, client: Client) -> None:
        assert MetatagArtistEntry.de_json({}, client) is None

    def test_de_json_required(self, client: Client, artist: Artist) -> None:
        json_dict: Dict[str, JSONType] = {'artist': artist.to_dict()}
        metatag_artist_entry = MetatagArtistEntry.de_json(json_dict, client)
        assert metatag_artist_entry is not None

        assert metatag_artist_entry.artist == artist
        assert metatag_artist_entry.popular_tracks == []

    def test_de_json_all(self, client: Client, artist: Artist, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'popularTracks': [track.to_dict()],
        }
        metatag_artist_entry = MetatagArtistEntry.de_json(json_dict, client)
        assert metatag_artist_entry is not None

        assert metatag_artist_entry.artist == artist
        assert metatag_artist_entry.popular_tracks == [track]

    def test_equality(self, artist: Artist, track: Track) -> None:
        a = MetatagArtistEntry(artist=artist, popular_tracks=[track])
        b = MetatagArtistEntry(artist=None, popular_tracks=[track])
        c = MetatagArtistEntry(artist=artist, popular_tracks=[track])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
