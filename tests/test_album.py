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
    text_color = '#000000'
    short_description = ''
    description = (
        'В начале 2015 года вокалист Asking Alexandria Дэнни Уорсноп объявил об уходе из группы — музыкант'
        ' стал строить сольную карьеру и заниматься другими проектами. Однако через неполных два года '
        'Уорсноп вернулся в группу, и в конце 2017-го музыканты представили пятую пластинку в прежнем '
        'составе. «Было здорово вернуться к ребятам. Думаю, нам всем нужно было время, чтобы отпустить '
        'то, что произошло между нами. Хорошо быть снова вместе», — говорит Денни Уорсноп.'
    )
    is_premiere = False
    is_banner = False
    meta_type = 'music'
    storage_dir = '4beeac1e.a.1155208'
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
    available_as_rbt = False
    lyrics_available = True
    remember_position = False
    duration_ms = 200440
    explicit = False
    start_date = '2020-06-30'
    likes_count = 2
    available_regions = ['kg', 'tm', 'by', 'kz', 'md', 'ru', 'am', 'ge', 'uz', 'tj', 'il', 'az', 'ua']

    def test_expected_values(
        self,
        album,
        artist_without_tracks,
        label,
        track_position,
        track_without_albums,
        album_without_nested_albums,
        deprecation,
    ):
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
        assert album.text_color == self.text_color
        assert album.short_description == self.short_description
        assert album.description == self.description
        assert album.is_premiere == self.is_premiere
        assert album.is_banner == self.is_banner
        assert album.meta_type == self.meta_type
        assert album.storage_dir == self.storage_dir
        assert album.og_image == self.og_image
        assert album.buy == self.buy
        assert album.recent == self.recent
        assert album.very_important == self.very_important
        assert album.available_for_mobile == self.available_for_mobile
        assert album.available_partially == self.available_partially
        assert album.bests == self.bests
        assert album.duplicates == [album_without_nested_albums]
        assert album.prerolls == self.prerolls
        assert album.volumes == [[track_without_albums]]
        assert album.year == self.year
        assert album.release_date == self.release_date
        assert album.type == self.type
        assert album.track_position == track_position
        assert album.regions == self.regions
        assert album.available_as_rbt == self.available_as_rbt
        assert album.lyrics_available == self.lyrics_available
        assert album.remember_position == self.remember_position
        assert album.duration_ms == self.duration_ms
        assert album.explicit == self.explicit
        assert album.start_date == self.start_date
        assert album.likes_count == self.likes_count
        assert album.deprecation == deprecation
        assert album.available_regions == self.available_regions

    def test_de_json_none(self, client):
        assert Album.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Album.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'id': self.id}
        album = Album.de_json(json_dict, client)

    def test_de_json_all(self, client, artist, label, track_position, track, album_without_nested_albums, deprecation):
        labels = [label] if type(label) == str else [label.to_dict()]
        json_dict = {
            'id': self.id,
            'error': self.error,
            'title': self.title,
            'cover_uri': self.cover_uri,
            'track_count': self.track_count,
            'artists': [artist.to_dict()],
            'labels': labels,
            'available': self.available,
            'available_for_premium_users': self.available_for_premium_users,
            'version': self.version,
            'content_warning': self.content_warning,
            'regions': self.regions,
            'original_release_year': self.original_release_year,
            'genre': self.genre,
            'buy': self.buy,
            'og_image': self.og_image,
            'recent': self.recent,
            'very_important': self.very_important,
            'available_for_mobile': self.available_for_mobile,
            'available_partially': self.available_partially,
            'bests': self.bests,
            'prerolls': self.prerolls,
            'volumes': [[track.to_dict()]],
            'year': self.year,
            'release_date': self.release_date,
            'type': self.type,
            'track_position': track_position.to_dict(),
            'meta_type': self.meta_type,
            'storage_dir': self.storage_dir,
            'is_banner': self.is_banner,
            'duplicates': [album_without_nested_albums.to_dict()],
            'is_premiere': self.is_premiere,
            'short_description': self.short_description,
            'description': self.description,
            'text_color': self.text_color,
            'available_as_rbt': self.available_as_rbt,
            'lyrics_available': self.lyrics_available,
            'remember_position': self.remember_position,
            'albums': [album_without_nested_albums.to_dict()],
            'duration_ms': self.duration_ms,
            'explicit': self.explicit,
            'start_date': self.start_date,
            'likes_count': self.likes_count,
            'deprecation': deprecation.to_dict(),
            'available_regions': self.available_regions,
        }
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
        assert album.text_color == self.text_color
        assert album.short_description == self.short_description
        assert album.description == self.description
        assert album.is_premiere == self.is_premiere
        assert album.is_banner == self.is_banner
        assert album.meta_type == self.meta_type
        assert album.storage_dir == self.storage_dir
        assert album.og_image == self.og_image
        assert album.buy == self.buy
        assert album.recent == self.recent
        assert album.very_important == self.very_important
        assert album.available_for_mobile == self.available_for_mobile
        assert album.available_partially == self.available_partially
        assert album.bests == self.bests
        assert album.duplicates == [album_without_nested_albums]
        assert album.prerolls == self.prerolls
        assert album.volumes == [[track]]
        assert album.year == self.year
        assert album.release_date == self.release_date
        assert album.type == self.type
        assert album.track_position == track_position
        assert album.regions == self.regions
        assert album.available_as_rbt == self.available_as_rbt
        assert album.lyrics_available == self.lyrics_available
        assert album.remember_position == self.remember_position
        assert album.duration_ms == self.duration_ms
        assert album.explicit == self.explicit
        assert album.start_date == self.start_date
        assert album.likes_count == self.likes_count
        assert album.deprecation == deprecation
        assert album.available_regions == self.available_regions

    def test_equality(self, artist, label):
        a = Album(self.id)
        b = Album(10)
        c = Album(self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
