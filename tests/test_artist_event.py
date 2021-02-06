from yandex_music import ArtistEvent


class TestArtistEvent:
    subscribed = True

    def test_expected_values(self, artist_event, artist, track):
        assert artist_event.artist == artist
        assert artist_event.tracks == [track]
        assert artist_event.similar_to_artists_from_history == [artist]
        assert artist_event.subscribed == self.subscribed

    def test_de_json_none(self, client):
        assert ArtistEvent.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert ArtistEvent.de_list({}, client) == []

    def test_de_json_required(self, client, artist, track):
        json_dict = {
            'artist': artist.to_dict(),
            'tracks': [track.to_dict()],
            'similar_to_artists_from_history': [artist.to_dict()],
        }
        artist_event = ArtistEvent.de_json(json_dict, client)

        assert artist_event.artist == artist
        assert artist_event.tracks == [track]
        assert artist_event.similar_to_artists_from_history == [artist]

    def test_de_json_all(self, client, artist, track):
        json_dict = {
            'artist': artist.to_dict(),
            'tracks': [track.to_dict()],
            'similar_to_artists_from_history': [artist.to_dict()],
            'subscribed': self.subscribed,
        }
        artist_event = ArtistEvent.de_json(json_dict, client)

        assert artist_event.artist == artist
        assert artist_event.tracks == [track]
        assert artist_event.similar_to_artists_from_history == [artist]
        assert artist_event.subscribed == self.subscribed

    def test_equality(self, artist, track):
        a = ArtistEvent(artist, [track], [artist])
        b = ArtistEvent(None, [track], [artist])
        c = ArtistEvent(artist, [track], [artist])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
