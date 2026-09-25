import asyncio
from typing import Any, Tuple
from unittest.mock import AsyncMock, MagicMock

from yandex_music import Client, ClientAsync, Track
from yandex_music.utils.request_base import default_timeout

DOWNLOAD_INFO_URL = 'https://storage.example.com/download-info/12345'
DOWNLOAD_INFO = [
    {
        'codec': 'mp3',
        'bitrateInKbps': 192,
        'gain': False,
        'preview': False,
        'downloadInfoUrl': DOWNLOAD_INFO_URL,
        'direct': False,
    }
]
XML = b'<download-info><host>cdn.example.com</host><path>/fake/path</path><ts>abc</ts><s>salt</s></download-info>'
FILE = b'fake-mp3-bytes'


def _make_track(client_class: Any, mock_class: Any) -> Tuple[Track, MagicMock]:
    request = MagicMock()
    request.get = mock_class(return_value=DOWNLOAD_INFO)
    request.retrieve = mock_class(side_effect=lambda url, **_: XML if url == DOWNLOAD_INFO_URL else FILE)
    request.download = mock_class(return_value=None)

    client = client_class()
    client._request = request

    return Track(id='12345', client=client), request


def _timeouts(mock: MagicMock) -> list:
    return [call.kwargs['timeout'] for call in mock.call_args_list]


class TestDownloadTimeout:
    def test_download_passes_timeout_to_every_request(self):
        track, request = _make_track(Client, MagicMock)

        track.download('track.mp3', timeout=30)

        assert _timeouts(request.get) == [30]
        assert _timeouts(request.retrieve) == [30]
        assert _timeouts(request.download) == [30]
        assert request.download.call_args.args[1] == 'track.mp3'

    def test_download_without_timeout_uses_client_default(self):
        track, request = _make_track(Client, MagicMock)

        track.download('track.mp3')

        assert _timeouts(request.get) == [default_timeout]
        assert _timeouts(request.retrieve) == [default_timeout]
        assert _timeouts(request.download) == [default_timeout]

    def test_download_bytes_passes_timeout_to_every_request(self):
        track, request = _make_track(Client, MagicMock)

        assert track.download_bytes(timeout=30) == FILE

        assert _timeouts(request.get) == [30]
        # первый запрос возвращает XML с прямой ссылкой, второй сам файл
        assert _timeouts(request.retrieve) == [30, 30]

    def test_download_async_passes_timeout_to_every_request(self):
        track, request = _make_track(ClientAsync, AsyncMock)

        asyncio.run(track.download_async('track.mp3', timeout=30))

        assert _timeouts(request.get) == [30]
        assert _timeouts(request.retrieve) == [30]
        assert _timeouts(request.download) == [30]

    def test_download_bytes_async_passes_timeout_to_every_request(self):
        track, request = _make_track(ClientAsync, AsyncMock)

        assert asyncio.run(track.download_bytes_async(timeout=30)) == FILE

        assert _timeouts(request.get) == [30]
        assert _timeouts(request.retrieve) == [30, 30]

    def test_download_info_download_positional_timeout(self):
        track, request = _make_track(Client, MagicMock)
        info = track.get_specific_download_info('mp3', 192)
        assert info is not None

        info.download('track.mp3', 30)

        assert _timeouts(request.retrieve) == [30]
        assert _timeouts(request.download) == [30]
