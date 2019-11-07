import pytest

from yandex_music import VideoSupplement


@pytest.fixture(scope='class')
def video_supplement():
    return VideoSupplement(TestVideoSupplement.cover, TestVideoSupplement.title, TestVideoSupplement.provider,
                           TestVideoSupplement.provider_video_id, TestVideoSupplement.url,
                           TestVideoSupplement.embed_url, TestVideoSupplement.embed)


class TestVideoSupplement:
    title = None
    provider = None
    provider_video_id = None
    url = None
    embed_url = None
    embed = None

    def test_expected_values(self, video_supplement, cover):
        assert video_supplement.cover == cover
        assert video_supplement.title == self.title
        assert video_supplement.provider == self.provider
        assert video_supplement.provider_video_id == self.provider_video_id
        assert video_supplement.url == self.url
        assert video_supplement.embed_url == self.embed_url
        assert video_supplement.embed == self.embed

    def test_de_json_required(self, client, cover):
        json_dict = {'cover': cover, 'title': self.title, 'provider': self.provider,
                     'provider_video_id': self.provider_video_id}
        video_supplement = VideoSupplement.de_json(json_dict, client)

        assert video_supplement.cover == cover
        assert video_supplement.title == self.title
        assert video_supplement.provider == self.provider
        assert video_supplement.provider_video_id == self.provider_video_id

    def test_de_json_all(self, client, cover):
        json_dict = {'cover': cover, 'title': self.title, 'provider': self.provider,
                     'provider_video_id': self.provider_video_id, 'url': self.url, 'embed_url': self.embed_url,
                     'embed': self.embed}
        video_supplement = VideoSupplement.de_json(json_dict, client)

        assert video_supplement.cover == cover
        assert video_supplement.title == self.title
        assert video_supplement.provider == self.provider
        assert video_supplement.provider_video_id == self.provider_video_id
        assert video_supplement.url == self.url
        assert video_supplement.embed_url == self.embed_url
        assert video_supplement.embed == self.embed

    def test_equality(self):
        pass
