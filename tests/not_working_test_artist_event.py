import pytest

from yandex_music import ArtistEvent


@pytest.fixture(scope='class')
def artist_event(artist, tracks, similar_to_artists_from_history):
    return ArtistEvent(artist, tracks, similar_to_artists_from_history)


class TestArtistEvent:

    def test_expected_values(self, artist_event, artist, tracks, similar_to_artists_from_history):
        assert artist_event.artist == artist
        assert artist_event.tracks == tracks
        assert artist_event.similar_to_artists_from_history == similar_to_artists_from_history

    def test_de_json_required(self, client, artist, tracks, similar_to_artists_from_history):
        json_dict = {'artist': artist, 'tracks': tracks,
                     'similar_to_artists_from_history': similar_to_artists_from_history}
        artist_event = ArtistEvent.de_json(json_dict, client)

        assert artist_event.artist == artist
        assert artist_event.tracks == tracks
        assert artist_event.similar_to_artists_from_history == similar_to_artists_from_history

    def test_de_json_all(self, client, artist, tracks, similar_to_artists_from_history):
        json_dict = {'artist': artist, 'tracks': tracks,
                     'similar_to_artists_from_history': similar_to_artists_from_history}
        artist_event = ArtistEvent.de_json(json_dict, client)

        assert artist_event.artist == artist
        assert artist_event.tracks == tracks
        assert artist_event.similar_to_artists_from_history == similar_to_artists_from_history

    def test_equality(self):
        pass
