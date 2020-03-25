from yandex_music import Album


class TestAlbum:
    id = 5239478
    error = 'not-found'
    title = 'In the End'
    version = 'feat. Mark Van Hoen & Mike Harding'
    cover_uri = 'avatars.yandex.net/get-music-content/95061/89c14a7d.a.5239478-1/%%'
    track_count = 3
    available = True
    available_for_premium_users = True
    content_warning = None
    original_release_year = None
    genre = 'alternative'
    og_image = 'avatars.yandex.net/get-music-content/95061/89c14a7d.a.5239478-1/%%'
    buy = []
    recent = False
    very_important = False
    available_for_mobile = True
    available_partially = False
    bests = [51241318]
    prerolls = None
    year = 2019
    release_date = '2019-03-22T00:00:00+03:00'
    type = 'single'
    regions = None

    def test_expected_values(self, album, artist_without_tracks, label, track_position, track_without_albums):
        assert album.id == self.id
        assert album.error == self.error
        assert album.title == self.title
        assert album.version == self.version
        assert album.cover_uri == self.cover_uri
        assert album.track_count == self.track_count
        assert album.artists == [artist_without_tracks]
        assert album.labels == [label]
        assert album.available == self.available
        assert album.available_for_premium_users == self.available_for_premium_users
        assert album.content_warning == self.content_warning
        assert album.original_release_year == self.original_release_year
        assert album.genre == self.genre
        assert album.og_image == self.og_image
        assert album.buy == self.buy
        assert album.recent == self.recent
        assert album.very_important == self.very_important
        assert album.available_for_mobile == self.available_for_mobile
        assert album.available_partially == self.available_partially
        assert album.bests == self.bests
        assert album.prerolls == self.prerolls
        assert album.volumes == [[track_without_albums]]
        assert album.year == self.year
        assert album.release_date == self.release_date
        assert album.type == self.type
        assert album.track_position == track_position
        assert album.regions == self.regions

    def test_de_json_none(self, client):
        assert Album.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Album.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'id_': self.id}
        album = Album.de_json(json_dict, client)

        assert album.id == self.id

    def test_de_json_all(self, client, artist, label, track_position, track):
        json_dict = {'id_': self.id, 'error': self.error, 'title': self.title, 'cover_uri': self.cover_uri,
                     'track_count': self.track_count, 'artists': [artist.to_dict()], 'labels': [label.to_dict()],
                     'available': self.available, 'available_for_premium_users': self.available_for_premium_users,
                     'version': self.version, 'content_warning': self.content_warning, 'regions': self.regions,
                     'original_release_year': self.original_release_year, 'genre': self.genre, 'buy': self.buy,
                     'og_image': self.og_image, 'recent': self.recent, 'very_important': self.very_important,
                     'available_for_mobile': self.available_for_mobile, 'available_partially': self.available_partially,
                     'bests': self.bests, 'prerolls': self.prerolls, 'volumes': [[track.to_dict()]], 'year': self.year,
                     'release_date': self.release_date, 'type_': self.type, 'track_position': track_position.to_dict()}
        album = Album.de_json(json_dict, client)

        assert album.id == self.id
        assert album.error == self.error
        assert album.title == self.title
        assert album.version == self.version
        assert album.cover_uri == self.cover_uri
        assert album.track_count == self.track_count
        assert album.artists == [artist]
        assert album.labels == [label]
        assert album.available == self.available
        assert album.available_for_premium_users == self.available_for_premium_users
        assert album.content_warning == self.content_warning
        assert album.original_release_year == self.original_release_year
        assert album.genre == self.genre
        assert album.og_image == self.og_image
        assert album.buy == self.buy
        assert album.recent == self.recent
        assert album.very_important == self.very_important
        assert album.available_for_mobile == self.available_for_mobile
        assert album.available_partially == self.available_partially
        assert album.bests == self.bests
        assert album.prerolls == self.prerolls
        assert album.volumes == [[track]]
        assert album.year == self.year
        assert album.release_date == self.release_date
        assert album.type == self.type
        assert album.track_position == track_position
        assert album.regions == self.regions

    def test_equality(self, artist, label):
        a = Album(self.id)
        b = Album(10)
        c = Album(self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
