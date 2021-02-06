from yandex_music import VideoSupplement


class TestVideoSupplement:
    title = 'pyrokinesis - терновый  венец  эволюции'
    provider = 'youtube'
    provider_video_id = '2lAjWy3Rzco'
    url = 'http://www.youtube.com/watch?v=2lAjWy3Rzco'
    embed_url = None
    embed = (
        '<iframe src="//www.youtube.com/embed/2lAjWy3Rzco?autoplay=1&amp;enablejsapi=1&amp;wmode=opaque" '
        'frameborder="0" scrolling="no" allowfullscreen="1" allow="autoplay; fullscreen; accelerometer; '
        'gyroscope; picture-in-picture" aria-label="Video"></iframe> '
    )
    cover = 'https://avatars.mds.yandex.net/get-vthumb/467750/8b52265a71a894918440ede6d63e45b5/%%x%%'

    def test_expected_values(self, video_supplement):
        assert video_supplement.cover == self.cover
        assert video_supplement.title == self.title
        assert video_supplement.provider == self.provider
        assert video_supplement.provider_video_id == self.provider_video_id
        assert video_supplement.url == self.url
        assert video_supplement.embed_url == self.embed_url
        assert video_supplement.embed == self.embed

    def test_de_json_none(self, client):
        assert VideoSupplement.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert VideoSupplement.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'cover': self.cover, 'provider': self.provider}
        video_supplement = VideoSupplement.de_json(json_dict, client)

        assert video_supplement.cover == self.cover
        assert video_supplement.provider == self.provider

    def test_de_json_all(self, client):
        json_dict = {
            'cover': self.cover,
            'title': self.title,
            'provider': self.provider,
            'provider_video_id': self.provider_video_id,
            'url': self.url,
            'embed_url': self.embed_url,
            'embed': self.embed,
        }
        video_supplement = VideoSupplement.de_json(json_dict, client)

        assert video_supplement.cover == self.cover
        assert video_supplement.title == self.title
        assert video_supplement.provider == self.provider
        assert video_supplement.provider_video_id == self.provider_video_id
        assert video_supplement.url == self.url
        assert video_supplement.embed_url == self.embed_url
        assert video_supplement.embed == self.embed

    def test_equality(self):
        a = VideoSupplement(self.cover, self.provider, self.title, self.provider_video_id)
        b = VideoSupplement(self.cover, self.provider, None, self.provider_video_id)
        c = VideoSupplement(self.cover, self.provider, self.title, self.provider_video_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
