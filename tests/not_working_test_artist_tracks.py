import pytest

from yandex_music import ArtistTracks


@pytest.fixture(scope='class')
def artist_tracks(tracks, pager):
    return ArtistTracks(tracks, pager)


class TestArtistTracks:

    def test_expected_values(self, artist_tracks, tracks, pager):
        assert artist_tracks.tracks == tracks
        assert artist_tracks.pager == pager

    def test_de_json_required(self, client, tracks, pager):
        json_dict = {'tracks': tracks, 'pager': pager}
        artist_tracks = ArtistTracks.de_json(json_dict, client)

        assert artist_tracks.tracks == tracks
        assert artist_tracks.pager == pager

    def test_de_json_all(self, client, tracks, pager):
        json_dict = {'tracks': tracks, 'pager': pager}
        artist_tracks = ArtistTracks.de_json(json_dict, client)

        assert artist_tracks.tracks == tracks
        assert artist_tracks.pager == pager

    def test_equality(self):
        pass
