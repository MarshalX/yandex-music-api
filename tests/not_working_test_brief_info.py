import pytest

from yandex_music import BriefInfo


@pytest.fixture(scope='class')
def brief_info(artist, albums, also_albums, popular_tracks, all_covers, videos, vinyls, playlist_ids, tracks_in_chart):
    return BriefInfo(artist, albums, also_albums, TestBriefInfo.last_release_ids, popular_tracks,
                     TestBriefInfo.similar_artists, all_covers, TestBriefInfo.concerts, videos, vinyls,
                     TestBriefInfo.has_promotions, playlist_ids, tracks_in_chart)


class TestBriefInfo:
    last_release_ids = None
    similar_artists = None
    concerts = None
    has_promotions = None

    def test_expected_values(self, brief_info, artist, albums, also_albums, popular_tracks, all_covers, videos, vinyls,
                             playlist_ids, tracks_in_chart):
        assert brief_info.artist == artist
        assert brief_info.albums == albums
        assert brief_info.also_albums == also_albums
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.popular_tracks == popular_tracks
        assert brief_info.similar_artists == self.similar_artists
        assert brief_info.all_covers == all_covers
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == videos
        assert brief_info.vinyls == vinyls
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == playlist_ids
        assert brief_info.tracks_in_chart == tracks_in_chart

    def test_de_json_required(self, client, artist, albums, also_albums, popular_tracks, all_covers, videos, vinyls,
                              playlist_ids):
        json_dict = {'artist': artist, 'albums': albums, 'also_albums': also_albums,
                     'last_release_ids': self.last_release_ids, 'popular_tracks': popular_tracks,
                     'similar_artists': self.similar_artists, 'all_covers': all_covers, 'concerts': self.concerts,
                     'videos': videos, 'vinyls': vinyls, 'has_promotions': self.has_promotions,
                     'playlist_ids': playlist_ids}
        brief_info = BriefInfo.de_json(json_dict, client)

        assert brief_info.artist == artist
        assert brief_info.albums == albums
        assert brief_info.also_albums == also_albums
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.popular_tracks == popular_tracks
        assert brief_info.similar_artists == self.similar_artists
        assert brief_info.all_covers == all_covers
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == videos
        assert brief_info.vinyls == vinyls
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == playlist_ids

    def test_de_json_all(self, client, artist, albums, also_albums, popular_tracks, all_covers, videos, vinyls,
                         playlist_ids, tracks_in_chart):
        json_dict = {'artist': artist, 'albums': albums, 'also_albums': also_albums,
                     'last_release_ids': self.last_release_ids, 'popular_tracks': popular_tracks,
                     'similar_artists': self.similar_artists, 'all_covers': all_covers, 'concerts': self.concerts,
                     'videos': videos, 'vinyls': vinyls, 'has_promotions': self.has_promotions,
                     'playlist_ids': playlist_ids, 'tracks_in_chart': tracks_in_chart}
        brief_info = BriefInfo.de_json(json_dict, client)

        assert brief_info.artist == artist
        assert brief_info.albums == albums
        assert brief_info.also_albums == also_albums
        assert brief_info.last_release_ids == self.last_release_ids
        assert brief_info.popular_tracks == popular_tracks
        assert brief_info.similar_artists == self.similar_artists
        assert brief_info.all_covers == all_covers
        assert brief_info.concerts == self.concerts
        assert brief_info.videos == videos
        assert brief_info.vinyls == vinyls
        assert brief_info.has_promotions == self.has_promotions
        assert brief_info.playlist_ids == playlist_ids
        assert brief_info.tracks_in_chart == tracks_in_chart

    def test_equality(self):
        pass
