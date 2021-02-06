import pytest

from yandex_music import BriefInfo


@pytest.fixture(scope='class')
def brief_info(artist, track, album, playlist, cover, playlist_id, video, chart, vinyl):
    return BriefInfo(
        artist,
        [album],
        [playlist],
        [album],
        TestBriefInfo.last_release_ids,
        [album],
        [track],
        [artist],
        [cover],
        TestBriefInfo.concerts,
        [video],
        [vinyl],
        TestBriefInfo.has_promotions,
        [playlist_id],
        [chart],
    )


class TestBriefInfo:
    last_release_ids = [8501194, 8302547, 8302836, 8302450]
    concerts = None
    has_promotions = False

    def test_expected_values(self, brief_info, artist, track, album, playlist, cover, playlist_id, video, chart, vinyl):
        assert brief_info.artist == artist
        assert brief_info.albums == [album]
        assert brief_info.playlists == [playlist]
        assert brief_info.also_albums == [album]
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.last_releases == [album]
        assert brief_info.popular_tracks == [track]
        assert brief_info.similar_artists == [artist]
        assert brief_info.all_covers == [cover]
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == [video]
        assert brief_info.vinyls == [vinyl]
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == [playlist_id]
        assert brief_info.tracks_in_chart == [chart]

    def test_de_json_none(self, client):
        assert BriefInfo.de_json({}, client) is None

    def test_de_json_required(self, client, artist, track, album, playlist, cover, playlist_id, video, vinyl):
        json_dict = {
            'artist': artist.to_dict(),
            'albums': [album.to_dict()],
            'also_albums': [album.to_dict()],
            'last_release_ids': self.last_release_ids,
            'last_releases': [album.to_dict()],
            'popular_tracks': [track.to_dict()],
            'similar_artists': [artist.to_dict()],
            'all_covers': [cover.to_dict()],
            'concerts': self.concerts,
            'videos': [video.to_dict()],
            'vinyls': [vinyl.to_dict()],
            'has_promotions': self.has_promotions,
            'playlist_ids': [playlist_id.to_dict()],
            'playlists': [playlist.to_dict()],
        }
        brief_info = BriefInfo.de_json(json_dict, client)

        assert brief_info.artist == artist
        assert brief_info.albums == [album]
        assert brief_info.playlists == [playlist]
        assert brief_info.also_albums == [album]
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.last_releases == [album]
        assert brief_info.popular_tracks == [track]
        assert brief_info.similar_artists == [artist]
        assert brief_info.all_covers == [cover]
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == [video]
        assert brief_info.vinyls == [vinyl]
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == [playlist_id]

    def test_de_json_all(self, client, artist, track, album, playlist, cover, playlist_id, video, chart, vinyl):
        json_dict = {
            'artist': artist.to_dict(),
            'albums': [album.to_dict()],
            'also_albums': [album.to_dict()],
            'last_release_ids': self.last_release_ids,
            'last_releases': [album.to_dict()],
            'popular_tracks': [track.to_dict()],
            'similar_artists': [artist.to_dict()],
            'all_covers': [cover.to_dict()],
            'concerts': self.concerts,
            'videos': [video.to_dict()],
            'vinyls': [vinyl.to_dict()],
            'has_promotions': self.has_promotions,
            'playlist_ids': [playlist_id.to_dict()],
            'tracks_in_chart': [chart.to_dict()],
            'playlists': [playlist.to_dict()],
        }
        brief_info = BriefInfo.de_json(json_dict, client)

        assert brief_info.artist == artist
        assert brief_info.albums == [album]
        assert brief_info.playlists == [playlist]
        assert brief_info.also_albums == [album]
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.last_releases == [album]
        assert brief_info.popular_tracks == [track]
        assert brief_info.similar_artists == [artist]
        assert brief_info.all_covers == [cover]
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == [video]
        assert brief_info.vinyls == [vinyl]
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == [playlist_id]
        assert brief_info.tracks_in_chart == [chart]

    def test_equality(self, artist, track, album, playlist, cover, playlist_id, video, vinyl):
        a = BriefInfo(
            artist,
            [album],
            [playlist],
            [album],
            self.last_release_ids,
            [album],
            [track],
            [artist],
            [cover],
            self.concerts,
            [video],
            [vinyl],
            self.has_promotions,
            [playlist_id],
        )
        b = BriefInfo(
            artist,
            [album],
            [],
            [album],
            self.last_release_ids,
            [],
            [],
            [artist],
            [cover],
            self.concerts,
            [video],
            [vinyl],
            True,
            [playlist_id],
        )
        c = BriefInfo(
            artist,
            [album],
            [playlist],
            [album],
            [1, 2, 3],
            [album],
            [track],
            [artist],
            [],
            self.concerts,
            [video],
            [vinyl],
            self.has_promotions,
            [playlist_id],
        )
        d = BriefInfo(
            artist,
            [album],
            [playlist],
            [album],
            self.last_release_ids,
            [album],
            [track],
            [artist],
            [cover],
            self.concerts,
            [video],
            [vinyl],
            self.has_promotions,
            [playlist_id],
        )

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
