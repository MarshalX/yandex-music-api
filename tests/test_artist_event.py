from typing import Dict

from yandex_music import Artist, ArtistEvent, Client, JSONType, Track


class TestArtistEvent:
    subscribed = True

    def test_expected_values(self, artist_event: ArtistEvent, artist: Artist, track: Track) -> None:
        assert artist_event.artist == artist
        assert artist_event.tracks == [track]
        assert artist_event.similar_to_artists_from_history == [artist]
        assert artist_event.subscribed == self.subscribed

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistEvent.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert ArtistEvent.de_list([], client) == []

    def test_de_json_required(self, client: Client, artist: Artist, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'tracks': [track.to_dict()],
            'similar_to_artists_from_history': [artist.to_dict()],
        }
        artist_event = ArtistEvent.de_json(json_dict, client)
        assert artist_event is not None

        assert artist_event.artist == artist
        assert artist_event.tracks == [track]
        assert artist_event.similar_to_artists_from_history == [artist]

    def test_de_json_all(self, client: Client, artist: Artist, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {
            'artist': artist.to_dict(),
            'tracks': [track.to_dict()],
            'similar_to_artists_from_history': [artist.to_dict()],
            'subscribed': self.subscribed,
        }
        artist_event = ArtistEvent.de_json(json_dict, client)
        assert artist_event is not None

        assert artist_event.artist == artist
        assert artist_event.tracks == [track]
        assert artist_event.similar_to_artists_from_history == [artist]
        assert artist_event.subscribed == self.subscribed

    def test_equality(self, artist: Artist, track: Track) -> None:
        a = ArtistEvent(artist, [track], [artist])
        b = ArtistEvent(None, [track], [artist])
        c = ArtistEvent(artist, [track], [artist])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
