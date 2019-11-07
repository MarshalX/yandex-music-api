from yandex_music import Track


class TestTrack:
    title = None
    available = None
    available_for_premium_users = None
    lyrics_available = None
    real_id = None
    og_image = None
    type = None
    cover_uri = None
    duration_ms = None
    storage_dir = None
    file_size = None
    error = None
    regions = None
    available_as_rbt = None
    content_warning = None
    explicit = None
    preview_duration_ms = None
    available_full_without_permission = None

    def test_expected_values(self, track, id, artists, albums, major, normalization):
        assert track.id == id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == artists
        assert track.albums == albums
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

    def test_de_json_required(self, client, id, artists, albums):
        json_dict = {'id': id, 'title': self.title, 'available': self.available,
                     'available_for_premium_users': self.available_for_premium_users, 'artists': artists,
                     'albums': albums, 'lyrics_available': self.lyrics_available}
        track = Track.de_json(json_dict, client)

        assert track.id == id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == artists
        assert track.albums == albums
        assert track.lyrics_available == self.lyrics_available

    def test_de_json_all(self, client, id, artists, albums, major, normalization):
        json_dict = {'id': id, 'title': self.title, 'available': self.available,
                     'available_for_premium_users': self.available_for_premium_users, 'artists': artists,
                     'albums': albums, 'lyrics_available': self.lyrics_available, 'real_id': self.real_id,
                     'og_image': self.og_image, 'type': self.type, 'cover_uri': self.cover_uri, 'major': major,
                     'duration_ms': self.duration_ms, 'storage_dir': self.storage_dir, 'file_size': self.file_size,
                     'normalization': normalization, 'error': self.error, 'regions': self.regions,
                     'available_as_rbt': self.available_as_rbt, 'content_warning': self.content_warning,
                     'explicit': self.explicit, 'preview_duration_ms': self.preview_duration_ms,
                     'available_full_without_permission': self.available_full_without_permission}
        track = Track.de_json(json_dict, client)

        assert track.id == id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == artists
        assert track.albums == albums
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

    def test_equality(self):
        pass
