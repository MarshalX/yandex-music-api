from yandex_music import Playlist


class TestPlaylist:
    uid = None
    kind = None
    title = None
    track_count = None
    tags = None
    revision = None
    snapshot = None
    visibility = None
    collective = None
    created = None
    modified = None
    available = None
    is_banner = None
    is_premiere = None
    duration_ms = None
    og_image = None
    prerolls = None
    likes_count = None
    generated_playlist_type = None
    animated_cover_uri = None
    ever_played = None
    description_formatted = None
    is_for_from = None
    regions = None

    def test_expected_values(self, playlist, owner, cover, made_for, play_counter, tracks, description):
        assert playlist.owner == owner
        assert playlist.uid == self.uid
        assert playlist.kind == self.kind
        assert playlist.title == self.title
        assert playlist.track_count == self.track_count
        assert playlist.cover == cover
        assert playlist.made_for == made_for
        assert playlist.play_counter == play_counter
        assert playlist.tags == self.tags
        assert playlist.revision == self.revision
        assert playlist.snapshot == self.snapshot
        assert playlist.visibility == self.visibility
        assert playlist.collective == self.collective
        assert playlist.created == self.created
        assert playlist.modified == self.modified
        assert playlist.available == self.available
        assert playlist.is_banner == self.is_banner
        assert playlist.is_premiere == self.is_premiere
        assert playlist.duration_ms == self.duration_ms
        assert playlist.og_image == self.og_image
        assert playlist.tracks == tracks
        assert playlist.prerolls == self.prerolls
        assert playlist.likes_count == self.likes_count
        assert playlist.generated_playlist_type == self.generated_playlist_type
        assert playlist.animated_cover_uri == self.animated_cover_uri
        assert playlist.ever_played == self.ever_played
        assert playlist.description == description
        assert playlist.description_formatted == self.description_formatted
        assert playlist.is_for_from == self.is_for_from
        assert playlist.regions == self.regions

    def test_de_json_required(self, client, owner, cover, made_for, play_counter):
        json_dict = {'owner': owner, 'uid': self.uid, 'kind': self.kind, 'title': self.title,
                     'track_count': self.track_count, 'cover': cover, 'made_for': made_for,
                     'play_counter': play_counter}
        playlist = Playlist.de_json(json_dict, client)

        assert playlist.owner == owner
        assert playlist.uid == self.uid
        assert playlist.kind == self.kind
        assert playlist.title == self.title
        assert playlist.track_count == self.track_count
        assert playlist.cover == cover
        assert playlist.made_for == made_for
        assert playlist.play_counter == play_counter

    def test_de_json_all(self, client, owner, cover, made_for, play_counter, tracks, description):
        json_dict = {'owner': owner, 'uid': self.uid, 'kind': self.kind, 'title': self.title,
                     'track_count': self.track_count, 'cover': cover, 'made_for': made_for,
                     'play_counter': play_counter, 'tags': self.tags, 'revision': self.revision,
                     'snapshot': self.snapshot, 'visibility': self.visibility, 'collective': self.collective,
                     'created': self.created, 'modified': self.modified, 'available': self.available,
                     'is_banner': self.is_banner, 'is_premiere': self.is_premiere, 'duration_ms': self.duration_ms,
                     'og_image': self.og_image, 'tracks': tracks, 'prerolls': self.prerolls,
                     'likes_count': self.likes_count, 'generated_playlist_type': self.generated_playlist_type,
                     'animated_cover_uri': self.animated_cover_uri, 'ever_played': self.ever_played,
                     'description': description, 'description_formatted': self.description_formatted,
                     'is_for_from': self.is_for_from, 'regions': self.regions}
        playlist = Playlist.de_json(json_dict, client)

        assert playlist.owner == owner
        assert playlist.uid == self.uid
        assert playlist.kind == self.kind
        assert playlist.title == self.title
        assert playlist.track_count == self.track_count
        assert playlist.cover == cover
        assert playlist.made_for == made_for
        assert playlist.play_counter == play_counter
        assert playlist.tags == self.tags
        assert playlist.revision == self.revision
        assert playlist.snapshot == self.snapshot
        assert playlist.visibility == self.visibility
        assert playlist.collective == self.collective
        assert playlist.created == self.created
        assert playlist.modified == self.modified
        assert playlist.available == self.available
        assert playlist.is_banner == self.is_banner
        assert playlist.is_premiere == self.is_premiere
        assert playlist.duration_ms == self.duration_ms
        assert playlist.og_image == self.og_image
        assert playlist.tracks == tracks
        assert playlist.prerolls == self.prerolls
        assert playlist.likes_count == self.likes_count
        assert playlist.generated_playlist_type == self.generated_playlist_type
        assert playlist.animated_cover_uri == self.animated_cover_uri
        assert playlist.ever_played == self.ever_played
        assert playlist.description == description
        assert playlist.description_formatted == self.description_formatted
        assert playlist.is_for_from == self.is_for_from
        assert playlist.regions == self.regions

    def test_equality(self):
        pass
