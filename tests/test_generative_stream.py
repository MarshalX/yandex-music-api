from yandex_music import GenerativeStream


class TestGenerativeStream:
    version = '0.92'

    def test_expected_values(self, generative_stream, generative_stream_data, generative_stream_info):
        assert generative_stream.data == generative_stream_data
        assert generative_stream.version == self.version
        assert generative_stream.stream == generative_stream_info

    def test_de_json_none(self, client):
        assert GenerativeStream.de_json({}, client) is None

    def test_de_json_all(self, client, generative_stream_data, generative_stream_info):
        json_dict = {
            'data': generative_stream_data.to_dict(),
            'version': self.version,
            'stream': generative_stream_info.to_dict(),
        }
        generative_stream = GenerativeStream.de_json(json_dict, client)

        assert generative_stream.data == generative_stream_data
        assert generative_stream.version == self.version
        assert generative_stream.stream == generative_stream_info

    def test_equality(self, generative_stream_data, generative_stream_info):
        a = GenerativeStream(generative_stream_data, self.version, generative_stream_info)
        b = GenerativeStream(generative_stream_data, '1.0', generative_stream_info)
        c = GenerativeStream(generative_stream_data, self.version, generative_stream_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
