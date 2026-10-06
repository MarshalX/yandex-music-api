from typing import Dict

from yandex_music import Client, GenerativeStream, GenerativeStreamData, GenerativeStreamInfo, JSONType


class TestGenerativeStream:
    version = '0.92'

    def test_expected_values(
        self,
        generative_stream: GenerativeStream,
        generative_stream_data: GenerativeStreamData,
        generative_stream_info: GenerativeStreamInfo,
    ) -> None:
        assert generative_stream.data == generative_stream_data
        assert generative_stream.version == self.version
        assert generative_stream.stream == generative_stream_info

    def test_de_json_none(self, client: Client) -> None:
        assert GenerativeStream.de_json({}, client) is None

    def test_de_json_all(
        self, client: Client, generative_stream_data: GenerativeStreamData, generative_stream_info: GenerativeStreamInfo
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'data': generative_stream_data.to_dict(),
            'version': self.version,
            'stream': generative_stream_info.to_dict(),
        }
        generative_stream = GenerativeStream.de_json(json_dict, client)
        assert generative_stream is not None

        assert generative_stream.data == generative_stream_data
        assert generative_stream.version == self.version
        assert generative_stream.stream == generative_stream_info

    def test_equality(
        self, generative_stream_data: GenerativeStreamData, generative_stream_info: GenerativeStreamInfo
    ) -> None:
        a = GenerativeStream(generative_stream_data, self.version, generative_stream_info)
        b = GenerativeStream(generative_stream_data, '1.0', generative_stream_info)
        c = GenerativeStream(generative_stream_data, self.version, generative_stream_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
