from yandex_music import TrackLyrics


class TestTrackLyrics:
    download_url = 'https://music-lyrics.s3-private.mds.yandex.net/8145339.f0f2e9e0/37320085?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221113T085654Z&X-Amz-SignedHeaders=host&X-Amz-Expires=86400&X-Amz-Credential=B8LQDON9RSp6Pcbw1Hxz%2F20221113%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=148de126a9ca9a91cb157e6032d178c39bf604d2e4acec6155d81e51090533ac'
    lyric_id = 8145339
    external_lyric_id = '8638863'
    writer = ['Mother Mother']

    def test_expected_values(self, track_lyrics, lyrics_major):
        assert track_lyrics.download_url == self.download_url
        assert track_lyrics.lyric_id == self.lyric_id
        assert track_lyrics.external_lyric_id == self.external_lyric_id
        assert track_lyrics.writers == self.writer
        assert track_lyrics.major == lyrics_major

    def test_de_json_none(self, client):
        assert TrackLyrics.de_json({}, client) is None

    def test_de_json_required(self, client, lyrics_major):
        json_dict = {
            'download_url': self.download_url,
            'lyric_id': self.lyric_id,
            'external_lyric_id': self.external_lyric_id,
            'writers': self.writer,
            'major': lyrics_major.to_dict(),
        }

        track_lyrics = TrackLyrics.de_json(json_dict, client)
        assert track_lyrics.download_url == self.download_url
        assert track_lyrics.lyric_id == self.lyric_id
        assert track_lyrics.external_lyric_id == self.external_lyric_id
        assert track_lyrics.writers == self.writer
        assert track_lyrics.major == lyrics_major

    def test_de_json_all(self, client, lyrics_major):
        json_dict = {
            'download_url': self.download_url,
            'lyric_id': self.lyric_id,
            'external_lyric_id': self.external_lyric_id,
            'writers': self.writer,
            'major': lyrics_major.to_dict(),
        }

        track_lyrics = TrackLyrics.de_json(json_dict, client)
        assert track_lyrics.download_url == self.download_url
        assert track_lyrics.lyric_id == self.lyric_id
        assert track_lyrics.external_lyric_id == self.external_lyric_id
        assert track_lyrics.writers == self.writer
        assert track_lyrics.major == lyrics_major

    def test_equality(self, lyrics_major):
        a = TrackLyrics(self.download_url, self.lyric_id, self.external_lyric_id, self.writer, lyrics_major)
        b = TrackLyrics(self.download_url, 50, self.external_lyric_id, self.writer, lyrics_major)
        c = TrackLyrics(self.download_url, self.lyric_id, self.external_lyric_id, self.writer, lyrics_major)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
