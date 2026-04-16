from yandex_music import Metatag


class TestMetatag:
    id = '5ddc2610e7c903105b40bc3a'
    cover_uri = 'avatars.yandex.net/get-music-misc/2406661/meta-tag.example.cover/%%'
    color = '#3779BC'
    liked = False
    station_id = 'genre:allrock'
    custom_wave_animation_url = 'https://music-custom-wave-media.s3.yandex.net/base.json'

    def test_expected_values(
        self,
        metatag,
        metatag_title,
        artist,
        album,
        playlist,
        metatag_sort_by_value,
    ):
        assert metatag.id == self.id
        assert metatag.cover_uri == self.cover_uri
        assert metatag.color == self.color
        assert metatag.title == metatag_title
        assert metatag.liked == self.liked
        assert metatag.station_id == self.station_id
        assert metatag.custom_wave_animation_url == self.custom_wave_animation_url
        assert metatag.artists == [artist]
        assert metatag.albums == [album]
        assert metatag.playlists == [playlist]
        assert metatag.tracks_sort_by_values == [metatag_sort_by_value]
        assert metatag.albums_sort_by_values == [metatag_sort_by_value]
        assert metatag.playlists_sort_by_values == [metatag_sort_by_value]

    def test_de_json_none(self, client):
        assert Metatag.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'id': self.id}
        metatag = Metatag.de_json(json_dict, client)

        assert metatag.id == self.id
        assert metatag.title is None
        assert metatag.artists == []
        assert metatag.albums == []
        assert metatag.playlists == []

    def test_de_json_all(
        self,
        client,
        metatag_title,
        artist,
        album,
        playlist,
        metatag_sort_by_value,
    ):
        json_dict = {
            'id': self.id,
            'coverUri': self.cover_uri,
            'color': self.color,
            'title': metatag_title.to_dict(),
            'liked': self.liked,
            'stationId': self.station_id,
            'customWaveAnimationUrl': self.custom_wave_animation_url,
            'artists': [artist.to_dict()],
            'albums': [album.to_dict()],
            'playlists': [playlist.to_dict()],
            'tracksSortByValues': [metatag_sort_by_value.to_dict()],
            'albumsSortByValues': [metatag_sort_by_value.to_dict()],
            'playlistsSortByValues': [metatag_sort_by_value.to_dict()],
        }
        metatag = Metatag.de_json(json_dict, client)

        assert metatag.id == self.id
        assert metatag.cover_uri == self.cover_uri
        assert metatag.color == self.color
        assert metatag.title == metatag_title
        assert metatag.liked == self.liked
        assert metatag.station_id == self.station_id
        assert metatag.custom_wave_animation_url == self.custom_wave_animation_url
        assert metatag.artists == [artist]
        assert metatag.albums == [album]
        assert metatag.playlists == [playlist]
        assert metatag.tracks_sort_by_values == [metatag_sort_by_value]
        assert metatag.albums_sort_by_values == [metatag_sort_by_value]
        assert metatag.playlists_sort_by_values == [metatag_sort_by_value]

    def test_equality(self):
        a = Metatag(id=self.id)
        b = Metatag(id='other')
        c = Metatag(id=self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
