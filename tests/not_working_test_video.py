import pytest

from yandex_music import Video


@pytest.fixture(scope='class')
def video():
    return Video(TestVideo.title, TestVideo.cover, TestVideo.embed_url, TestVideo.provider, TestVideo.provider_video_id,
                 TestVideo.youtube_url, TestVideo.thumbnail_url, TestVideo.duration, TestVideo.text,
                 TestVideo.html_auto_play_video_player, TestVideo.regions)


class TestVideo:
    title = None
    embed_url = None
    provider = None
    provider_video_id = None
    youtube_url = None
    thumbnail_url = None
    duration = None
    text = None
    html_auto_play_video_player = None
    regions = None

    def test_expected_values(self, video, cover):
        assert video.title == self.title
        assert video.cover == cover
        assert video.embed_url == self.embed_url
        assert video.provider == self.provider
        assert video.provider_video_id == self.provider_video_id
        assert video.youtube_url == self.youtube_url
        assert video.thumbnail_url == self.thumbnail_url
        assert video.duration == self.duration
        assert video.text == self.text
        assert video.html_auto_play_video_player == self.html_auto_play_video_player
        assert video.regions == self.regions

    def test_de_json_required(self, client):
        json_dict = {'title': self.title}
        video = Video.de_json(json_dict, client)

        assert video.title == self.title

    def test_de_json_all(self, client, cover):
        json_dict = {'title': self.title, 'cover': cover, 'embed_url': self.embed_url, 'provider': self.provider,
                     'provider_video_id': self.provider_video_id, 'youtube_url': self.youtube_url,
                     'thumbnail_url': self.thumbnail_url, 'duration': self.duration, 'text': self.text,
                     'html_auto_play_video_player': self.html_auto_play_video_player, 'regions': self.regions}
        video = Video.de_json(json_dict, client)

        assert video.title == self.title
        assert video.cover == cover
        assert video.embed_url == self.embed_url
        assert video.provider == self.provider
        assert video.provider_video_id == self.provider_video_id
        assert video.youtube_url == self.youtube_url
        assert video.thumbnail_url == self.thumbnail_url
        assert video.duration == self.duration
        assert video.text == self.text
        assert video.html_auto_play_video_player == self.html_auto_play_video_player
        assert video.regions == self.regions

    def test_equality(self):
        pass
