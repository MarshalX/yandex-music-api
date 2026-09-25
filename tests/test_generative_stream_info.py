from yandex_music import GenerativeStreamInfo


class TestGenerativeStreamInfo:
    id = 'fake-stream-id'
    url = 'https://example.com/generative/stream.m3u8'

    def test_expected_values(self, generative_stream_info):
        assert generative_stream_info.id == self.id
        assert generative_stream_info.url == self.url

    def test_de_json_none(self, client):
        assert GenerativeStreamInfo.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'id': self.id, 'url': self.url}
        generative_stream_info = GenerativeStreamInfo.de_json(json_dict, client)

        assert generative_stream_info.id == self.id
        assert generative_stream_info.url == self.url

    def test_equality(self):
        a = GenerativeStreamInfo(self.id, self.url)
        b = GenerativeStreamInfo('other-stream-id', self.url)
        c = GenerativeStreamInfo(self.id, self.url)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
