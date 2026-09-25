from yandex_music import GenerativeStreamData


class TestGenerativeStreamData:
    title = 'Вдохновение'
    subtitle = 'Алгоритмы feat. Нейросеть'
    background_color = '#E5AA73'
    image_url = 'avatars.yandex.net/get-music-misc/12345/generative-focus-image/%%'
    video_cover_uri = 'https://example.com/generative/focus.mp4'
    explanations = 'Музыка, которая поможет сфокусироваться'

    def test_expected_values(self, generative_stream_data, cover_derived_colors):
        assert generative_stream_data.title == self.title
        assert generative_stream_data.subtitle == self.subtitle
        assert generative_stream_data.background_color == self.background_color
        assert generative_stream_data.derived_colors == cover_derived_colors
        assert generative_stream_data.image_url == self.image_url
        assert generative_stream_data.video_cover_uri == self.video_cover_uri
        assert generative_stream_data.explanations == self.explanations

    def test_de_json_none(self, client):
        assert GenerativeStreamData.de_json({}, client) is None

    def test_de_json_all(self, client, cover_derived_colors):
        json_dict = {
            'title': self.title,
            'subtitle': self.subtitle,
            'backgroundColor': self.background_color,
            'derivedColors': cover_derived_colors.to_dict(),
            'imageUrl': self.image_url,
            'videoCoverUri': self.video_cover_uri,
            'explanations': self.explanations,
        }
        generative_stream_data = GenerativeStreamData.de_json(json_dict, client)

        assert generative_stream_data.title == self.title
        assert generative_stream_data.subtitle == self.subtitle
        assert generative_stream_data.background_color == self.background_color
        assert generative_stream_data.derived_colors == cover_derived_colors
        assert generative_stream_data.image_url == self.image_url
        assert generative_stream_data.video_cover_uri == self.video_cover_uri
        assert generative_stream_data.explanations == self.explanations

    def test_equality(self):
        a = GenerativeStreamData(self.title, image_url=self.image_url)
        b = GenerativeStreamData('Бодрость', image_url=self.image_url)
        c = GenerativeStreamData(self.title, image_url=self.image_url)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
