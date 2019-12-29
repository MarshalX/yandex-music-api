from yandex_music import Playlist


class TestPlaylist:
    uid = 503646255
    kind = 69814820
    title = 'Плейлист дня'
    track_count = 57
    tags = []
    revision = 0
    snapshot = 1
    visibility = 'public'
    collective = False
    created = '2018-04-29T21:00:00+00:00'
    modified = '2019-11-09T03:00:00+00:00'
    available = True
    is_banner = False
    is_premiere = False
    duration_ms = 12402690
    og_image = 'avatars.yandex.net/get-music-user-playlist/38125/q0ahkhfQE3neTk/%%?1572609906461'
    prerolls = []
    likes_count = 1
    generated_playlist_type = 'playlistOfTheDay'
    animated_cover_uri = 'avatars.yandex.net/get-music-user-playlist/30088/q0ahjvoZK5FT4A/%%'
    ever_played = True
    description = 'Каждый день — новый. Каждый день — ваш!'
    description_formatted = 'Каждый день — новый. Каждый день — ваш!'
    is_for_from = None
    regions = None

    def test_expected_values(self, playlist, user, cover, made_for, track_short, play_counter, playlist_absence):
        assert playlist.owner == user
        assert playlist.uid == self.uid
        assert playlist.kind == self.kind
        assert playlist.title == self.title
        assert playlist.track_count == self.track_count
        assert playlist.cover == cover
        assert playlist.made_for == made_for
        assert playlist.play_counter == play_counter
        assert playlist.playlist_absence == playlist_absence
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
        assert playlist.tracks == [track_short]
        assert playlist.prerolls == self.prerolls
        assert playlist.likes_count == self.likes_count
        assert playlist.generated_playlist_type == self.generated_playlist_type
        assert playlist.animated_cover_uri == self.animated_cover_uri
        assert playlist.ever_played == self.ever_played
        assert playlist.description == self.description
        assert playlist.description_formatted == self.description_formatted
        assert playlist.is_for_from == self.is_for_from
        assert playlist.regions == self.regions

    def test_de_json_none(self, client):
        assert Playlist.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Playlist.de_list({}, client) == []

    def test_de_json_required(self, client, user, cover, made_for, play_counter, playlist_absence):
        json_dict = {'owner': user.to_dict(), 'uid': self.uid, 'kind': self.kind, 'title': self.title,
                     'track_count': self.track_count, 'cover': cover.to_dict(), 'made_for': made_for.to_dict(),
                     'play_counter': play_counter.to_dict(), 'playlist_absence': playlist_absence.to_dict()}
        playlist = Playlist.de_json(json_dict, client)

        assert playlist.owner == user
        assert playlist.uid == self.uid
        assert playlist.kind == self.kind
        assert playlist.title == self.title
        assert playlist.track_count == self.track_count
        assert playlist.cover == cover
        assert playlist.made_for == made_for
        assert playlist.play_counter == play_counter

    def test_de_json_all(self, client, user, cover, made_for, track_short, play_counter, playlist_absence):
        json_dict = {'owner': user.to_dict(), 'uid': self.uid, 'kind': self.kind, 'title': self.title,
                     'track_count': self.track_count, 'cover': cover.to_dict(), 'made_for': made_for.to_dict(),
                     'play_counter': play_counter.to_dict(), 'playlist_absence': playlist_absence.to_dict(),
                     'tags': self.tags, 'revision': self.revision, 'snapshot': self.snapshot,
                     'visibility': self.visibility, 'collective': self.collective, 'created': self.created,
                     'modified': self.modified, 'available': self.available, 'is_banner': self.is_banner,
                     'is_premiere': self.is_premiere, 'duration_ms': self.duration_ms, 'og_image': self.og_image,
                     'tracks': [track_short.to_dict()], 'prerolls': self.prerolls, 'likes_count': self.likes_count,
                     'generated_playlist_type': self.generated_playlist_type,
                     'animated_cover_uri': self.animated_cover_uri, 'ever_played': self.ever_played,
                     'description': self.description, 'description_formatted': self.description_formatted,
                     'is_for_from': self.is_for_from, 'regions': self.regions}
        playlist = Playlist.de_json(json_dict, client)

        assert playlist.owner == user
        assert playlist.uid == self.uid
        assert playlist.kind == self.kind
        assert playlist.title == self.title
        assert playlist.track_count == self.track_count
        assert playlist.cover == cover
        assert playlist.made_for == made_for
        assert playlist.play_counter == play_counter
        assert playlist.playlist_absence == playlist_absence
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
        assert playlist.tracks == [track_short]
        assert playlist.prerolls == self.prerolls
        assert playlist.likes_count == self.likes_count
        assert playlist.generated_playlist_type == self.generated_playlist_type
        assert playlist.animated_cover_uri == self.animated_cover_uri
        assert playlist.ever_played == self.ever_played
        assert playlist.description == self.description
        assert playlist.description_formatted == self.description_formatted
        assert playlist.is_for_from == self.is_for_from
        assert playlist.regions == self.regions

    def test_equality(self, user, cover, made_for, play_counter, playlist_absence):
        a = Playlist(user, cover, made_for, play_counter, playlist_absence)
        b = Playlist(user, cover, made_for, play_counter, None)
        c = Playlist(user, None, made_for, play_counter, playlist_absence)
        d = Playlist(user, cover, made_for, play_counter, playlist_absence)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
