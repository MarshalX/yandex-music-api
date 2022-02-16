from yandex_music import Track


class TestTrack:
    id = '10994777'
    title = 'Sapphire'
    available = True
    available_for_premium_users = True
    lyrics_available = False
    best = False
    real_id = '10994777'
    og_image = 'avatars.yandex.net/get-music-content/28589/daef4251.a.1193829-1/%%'
    type = 'music'
    cover_uri = 'avatars.yandex.net/get-music-content/28589/daef4251.a.1193829-1/%%'
    duration_ms = 251270
    storage_dir = '51327_109b74ca.36526310.1.609676'
    file_size = 6036792
    error = None
    can_publish = False
    state = 'playable'
    desired_visibility = 'private'
    filename = 'Ты не так плох.mp3'
    regions = None
    available_as_rbt = None
    content_warning = None
    explicit = None
    preview_duration_ms = 30000
    available_full_without_permission = False
    version = 'Radio Edit'
    remember_position = False
    background_video_uri = 'https://music-background-videos.s3.yandex.net/converted/60018e4cdcaa9a42948cda8d'
    short_description = (
        'По каким признакам во внешности, в поведении, в одежде можно понять, что девушка несвободна?'
        ' Чтобы не ошибиться со своими чувствами и устремлениями…» — такой замечательный вопрос'
        ' пришел мне от подписчика. Причин, которые могут остановить мужчин в момент появления'
        ' желания познакомиться с девушкой, достаточно много. Обычно они сводятся к опасениям,'
    )
    is_suitable_for_children = True

    def test_expected_values(
        self,
        track,
        artist,
        album,
        major,
        normalization,
        track_without_nested_tracks,
        user,
        meta_data,
        poetry_lover_match,
    ):
        assert track.id == self.id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == [artist]
        assert track.albums == [album]
        assert track.lyrics_available == self.lyrics_available
        assert track.poetry_lover_matches == [poetry_lover_match]
        assert track.best == self.best
        assert track.real_id == self.real_id
        assert track.og_image == self.og_image
        assert track.type == self.type
        assert track.cover_uri == self.cover_uri
        assert track.major == major
        assert track.duration_ms == self.duration_ms
        assert track.storage_dir == self.storage_dir
        assert track.file_size == self.file_size
        assert track.substituted == track_without_nested_tracks
        assert track.matched_track == track_without_nested_tracks
        assert track.normalization == normalization
        assert track.error == self.error
        assert track.meta_data == meta_data
        assert track.regions == self.regions
        assert track.available_as_rbt == self.available_as_rbt
        assert track.content_warning == self.content_warning
        assert track.explicit == self.explicit
        assert track.preview_duration_ms == self.preview_duration_ms
        assert track.available_full_without_permission == self.available_full_without_permission
        assert track.version == self.version
        assert track.remember_position == self.remember_position
        assert track.can_publish == self.can_publish
        assert track.state == self.state
        assert track.desired_visibility == self.desired_visibility
        assert track.filename == self.filename
        assert track.user_info == user
        assert track.background_video_uri == self.background_video_uri
        assert track.short_description == self.short_description
        assert track.is_suitable_for_children == self.is_suitable_for_children

    def test_de_json_none(self, client):
        assert Track.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Track.de_list({}, client) == []

    def test_de_json_required(self, client, artist, album):
        json_dict = {'id': self.id}
        track = Track.de_json(json_dict, client)

        assert track.id == self.id

    def test_de_json_all(
        self,
        client,
        artist,
        album,
        major,
        normalization,
        track_without_nested_tracks,
        user,
        meta_data,
        poetry_lover_match,
    ):
        json_dict = {
            'id': self.id,
            'title': self.title,
            'available': self.available,
            'available_for_premium_users': self.available_for_premium_users,
            'artists': [artist.to_dict()],
            'albums': [album.to_dict()],
            'lyrics_available': self.lyrics_available,
            'best': self.best,
            'real_id': self.real_id,
            'og_image': self.og_image,
            'type': self.type,
            'cover_uri': self.cover_uri,
            'major': major.to_dict(),
            'duration_ms': self.duration_ms,
            'storage_dir': self.storage_dir,
            'file_size': self.file_size,
            'normalization': normalization.to_dict(),
            'error': self.error,
            'regions': self.regions,
            'available_as_rbt': self.available_as_rbt,
            'content_warning': self.content_warning,
            'explicit': self.explicit,
            'preview_duration_ms': self.preview_duration_ms,
            'version': self.version,
            'available_full_without_permission': self.available_full_without_permission,
            'remember_position': self.remember_position,
            'substituted': track_without_nested_tracks.to_dict(),
            'matched_track': track_without_nested_tracks.to_dict(),
            'can_publish': self.can_publish,
            'state': self.state,
            'desired_visibility': self.desired_visibility,
            'filename': self.filename,
            'user_info': user.to_dict(),
            'meta_data': meta_data.to_dict(),
            'poetry_lover_matches': [poetry_lover_match.to_dict()],
            'background_video_uri': self.background_video_uri,
            'short_description': self.short_description,
            'is_suitable_for_children': self.is_suitable_for_children,
        }
        track = Track.de_json(json_dict, client)

        assert track.id == self.id
        assert track.title == self.title
        assert track.available == self.available
        assert track.available_for_premium_users == self.available_for_premium_users
        assert track.artists == [artist]
        assert track.albums == [album]
        assert track.lyrics_available == self.lyrics_available
        assert track.poetry_lover_matches == [poetry_lover_match]
        assert track.best == self.best
        assert track.real_id == self.real_id
        assert track.og_image == self.og_image
        assert track.type == self.type
        assert track.cover_uri == self.cover_uri
        assert track.major == major
        assert track.duration_ms == self.duration_ms
        assert track.storage_dir == self.storage_dir
        assert track.file_size == self.file_size
        assert track.substituted == track_without_nested_tracks
        assert track.matched_track == track_without_nested_tracks
        assert track.normalization == normalization
        assert track.error == self.error
        assert track.meta_data == meta_data
        assert track.regions == self.regions
        assert track.available_as_rbt == self.available_as_rbt
        assert track.content_warning == self.content_warning
        assert track.explicit == self.explicit
        assert track.preview_duration_ms == self.preview_duration_ms
        assert track.available_full_without_permission == self.available_full_without_permission
        assert track.version == self.version
        assert track.remember_position == self.remember_position
        assert track.can_publish == self.can_publish
        assert track.state == self.state
        assert track.desired_visibility == self.desired_visibility
        assert track.filename == self.filename
        assert track.user_info == user
        assert track.background_video_uri == self.background_video_uri
        assert track.short_description == self.short_description
        assert track.is_suitable_for_children == self.is_suitable_for_children

    def test_equality(self):
        a = Track(self.id)
        b = Track(10)
        c = Track(self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
