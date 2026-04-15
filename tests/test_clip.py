from yandex_music import Clip


class TestClip:
    clip_id = 12345
    title = 'Тестовый клип'
    version = 'Live'
    player_id = '1234567890123456789'
    uuid = 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6'
    thumbnail = 'https://avatars.yandex.net/get-music-content/12345/test-clip/%%'
    preview_url = 'https://video-preview.s3.yandex.net/vh/1234567890123456789/360p.mp4'
    duration = 240
    track_ids = [100500, 200600]
    disclaimers = ['explicit']
    explicit = True

    def test_expected_value(self, clip):
        assert clip.clip_id == self.clip_id
        assert clip.title == self.title
        assert clip.version == self.version
        assert clip.player_id == self.player_id
        assert clip.uuid == self.uuid
        assert clip.thumbnail == self.thumbnail
        assert clip.preview_url == self.preview_url
        assert clip.duration == self.duration
        assert clip.track_ids == self.track_ids
        assert clip.disclaimers == self.disclaimers
        assert clip.explicit == self.explicit

    def test_de_json_none(self, client):
        assert Clip.de_json({}, client) is None

    def test_de_json_all(self, client, artist):
        json_dict = {
            'clipId': self.clip_id,
            'title': self.title,
            'version': self.version,
            'playerId': self.player_id,
            'uuid': self.uuid,
            'thumbnail': self.thumbnail,
            'previewUrl': self.preview_url,
            'duration': self.duration,
            'trackIds': self.track_ids,
            'artists': [artist.to_dict()],
            'disclaimers': self.disclaimers,
            'explicit': self.explicit,
        }
        clip = Clip.de_json(json_dict, client)

        assert clip.clip_id == self.clip_id
        assert clip.title == self.title
        assert clip.version == self.version
        assert clip.player_id == self.player_id
        assert clip.uuid == self.uuid
        assert clip.thumbnail == self.thumbnail
        assert clip.preview_url == self.preview_url
        assert clip.duration == self.duration
        assert clip.track_ids == self.track_ids
        assert clip.artists == [artist]
        assert clip.disclaimers == self.disclaimers
        assert clip.explicit == self.explicit

    def test_equality(self):
        a = Clip(clip_id=self.clip_id)
        b = Clip(clip_id=99999)
        c = Clip(clip_id=self.clip_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
