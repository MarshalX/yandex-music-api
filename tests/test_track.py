from yandex_music import Track


class TestTrack:
    id = '10994777'
    title = 'Sapphire'
    available = True
    available_for_premium_users = True
    lyrics_available = False
    real_id = '10994777'
    og_image = 'avatars.yandex.net/get-music-content/28589/daef4251.a.1193829-1/%%'
    type = 'music'
    cover_uri = 'avatars.yandex.net/get-music-content/28589/daef4251.a.1193829-1/%%'
    duration_ms = 251270
    storage_dir = '51327_109b74ca.36526310.1.609676'
    file_size = 6036792
    error = None
    regions = None
    available_as_rbt = None
    content_warning = None
    explicit = None
    preview_duration_ms = 30000
    available_full_without_permission = False
    version = 'Radio Edit'
    remember_position = False

    def test_expected_values(self, track, artist, album, major, normalization):
        assert track.id == self.id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == [artist]
        assert track.albums == [album]
        assert track.lyrics_available == self.lyrics_available
        assert track.real_id == self.real_id
        assert track.og_image == self.og_image
        assert track.type == self.type
        assert track.cover_uri == self.cover_uri
        assert track.major == major
        assert track.duration_ms == self.duration_ms
        assert track.storage_dir == self.storage_dir
        assert track.file_size == self.file_size
        assert track.normalization == normalization
        assert track.error == self.error
        assert track.regions == self.regions
        assert track.available_as_rbt == self.available_as_rbt
        assert track.content_warning == self.content_warning
        assert track.explicit == self.explicit
        assert track.preview_duration_ms == self.preview_duration_ms
        assert track.available_full_without_permission == self.available_full_without_permission
        assert track.version == self.version
        assert track.remember_position == self.remember_position

    def test_de_json_none(self, client):
        assert Track.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Track.de_list({}, client) == []

    def test_de_json_required(self, client, artist, album):
        json_dict = {'id_': self.id, 'title': self.title, 'available': self.available,
                     'artists': [artist.to_dict()], 'albums': [album.to_dict()]}
        track = Track.de_json(json_dict, client)

        assert track.id == self.id
        assert track.title == self.title
        assert track.available == self.available
        assert track.artists == [artist]
        assert track.albums == [album]

    def test_de_json_all(self, client, artist, album, major, normalization):
        json_dict = {'id_': self.id, 'title': self.title, 'available': self.available,
                     'available_for_premium_users': self.available_for_premium_users,
                     'artists': [artist.to_dict()], 'albums': [album.to_dict()],
                     'lyrics_available': self.lyrics_available, 'real_id': self.real_id,
                     'og_image': self.og_image, 'type_': self.type, 'cover_uri': self.cover_uri,
                     'major': major.to_dict(), 'duration_ms': self.duration_ms, 'storage_dir': self.storage_dir,
                     'file_size': self.file_size, 'normalization': normalization.to_dict(), 'error': self.error,
                     'regions': self.regions, 'available_as_rbt': self.available_as_rbt,
                     'content_warning': self.content_warning, 'explicit': self.explicit,
                     'preview_duration_ms': self.preview_duration_ms, 'version': self.version,
                     'available_full_without_permission': self.available_full_without_permission,
                     'remember_position': self.remember_position}
        track = Track.de_json(json_dict, client)

        assert track.id == self.id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == [artist]
        assert track.albums == [album]
        assert track.lyrics_available == self.lyrics_available
        assert track.real_id == self.real_id
        assert track.og_image == self.og_image
        assert track.type == self.type
        assert track.cover_uri == self.cover_uri
        assert track.major == major
        assert track.duration_ms == self.duration_ms
        assert track.storage_dir == self.storage_dir
        assert track.file_size == self.file_size
        assert track.normalization == normalization
        assert track.error == self.error
        assert track.regions == self.regions
        assert track.available_as_rbt == self.available_as_rbt
        assert track.content_warning == self.content_warning
        assert track.explicit == self.explicit
        assert track.preview_duration_ms == self.preview_duration_ms
        assert track.available_full_without_permission == self.available_full_without_permission
        assert track.version == self.version
        assert track.remember_position == self.remember_position

    def test_equality(self, artist, album):
        a = Track(self.id, self.title, self.available, [artist], [album])
        b = Track(self.id, '', self.available, [artist], [])
        c = Track(self.id, self.title, self.available, [artist], [album])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
