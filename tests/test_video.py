from typing import Dict, List, Optional

from yandex_music import Client, JSONType, Video


class TestVideo:
    cover = 'https://avatars.mds.yandex.net/get-vh/1427422/10413967802532191922-QdZD9kEoIbQknQSxuy2zaQ-1557613291/%%'
    title = 'Back to Beautiful'
    embed_url = 'https://frontend.vh.yandex.ru/player/10413967802532191922?no_ad=true&from=ya-music'
    provider = 'yandex'
    provider_video_id = '10413967802532191922'
    youtube_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    text: Optional[str] = None
    html_auto_play_video_player: Optional[str] = None
    regions: Optional[List[str]] = None

    def test_expected_values(self, video: Video) -> None:
        assert video.title == self.title
        assert video.cover == self.cover
        assert video.embed_url == self.embed_url
        assert video.provider == self.provider
        assert video.provider_video_id == self.provider_video_id
        assert video.youtube_url == self.youtube_url
        assert video.thumbnail_url == self.thumbnail_url
        assert video.duration == self.duration
        assert video.text == self.text
        assert video.html_auto_play_video_player == self.html_auto_play_video_player
        assert video.regions == self.regions

    def test_de_json_none(self, client: Client) -> None:
        assert Video.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Video.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'title': self.title}
        video = Video.de_json(json_dict, client)
        assert video is not None

        assert video.title == self.title

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'cover': self.cover,
            'embed_url': self.embed_url,
            'provider': self.provider,
            'provider_video_id': self.provider_video_id,
            'youtube_url': self.youtube_url,
            'thumbnail_url': self.thumbnail_url,
            'duration': self.duration,
            'text': self.text,
            'html_auto_play_video_player': self.html_auto_play_video_player,
            'regions': self.regions,
        }
        video = Video.de_json(json_dict, client)
        assert video is not None

        assert video.title == self.title
        assert video.cover == self.cover
        assert video.embed_url == self.embed_url
        assert video.provider == self.provider
        assert video.provider_video_id == self.provider_video_id
        assert video.youtube_url == self.youtube_url
        assert video.thumbnail_url == self.thumbnail_url
        assert video.duration == self.duration
        assert video.text == self.text
        assert video.html_auto_play_video_player == self.html_auto_play_video_player
        assert video.regions == self.regions

    def test_equality(self) -> None:
        a = Video(self.title, '', provider_video_id=self.provider_video_id)
        b = Video('', self.cover, self.embed_url)
        c = Video(self.title, provider_video_id=self.provider_video_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
