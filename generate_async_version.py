#!/usr/bin/env python3
"""Generate async version of client.py and request.py."""
import subprocess

DISCLAIMER = "# THIS IS AUTO GENERATED COPY OF client.py. DON'T EDIT IN BY HANDS #"
DISCLAIMER = f'{"#" * len(DISCLAIMER)}\n{DISCLAIMER}\n{"#" * len(DISCLAIMER)}\n\n'

REQUEST_METHODS = ('_request_wrapper', 'get', 'post', 'retrieve', 'download')


def gen_request(output_request_filename: str) -> None:
    """Generate async version of request.py."""
    with open('yandex_music/utils/request.py', 'r', encoding='UTF-8') as f:
        code = f.read()

    code = code.replace('import requests', 'import asyncio\nimport aiohttp\nimport aiofiles')

    # order make sense
    code = code.replace('resp.content', 'content')
    code = code.replace(
        'resp = requests.request(*args, **kwargs)',
        f'async with aiohttp.request(*args, **kwargs) as _resp:\n{" " * 16}resp = _resp\n{" " * 16}content = await resp.content.read()',  # noqa: E501
    )

    code = code.replace('except requests.Timeout', 'except asyncio.TimeoutError')
    code = code.replace('except requests.RequestException', 'except aiohttp.ClientError')
    code = code.replace('resp.status_code', 'resp.status')

    for method in REQUEST_METHODS:
        code = code.replace(f'def {method}', f'async def {method}')
        code = code.replace(f'self.{method}(', f'await self.{method}(')

    code = code.replace('proxies=self.proxies', 'proxy=self.proxy_url')
    code = code.replace(
        "kwargs['timeout'] = self._timeout",
        f"kwargs['timeout'] = aiohttp.ClientTimeout(total=self._timeout)\n{' ' * 8}else:\n{' ' * 12}kwargs['timeout'] = aiohttp.ClientTimeout(total=kwargs['timeout'])",  # noqa: E501
    )

    # download method
    code = code.replace('with open', 'async with aiofiles.open')
    code = code.replace('f.write', 'await f.write')

    # docs
    code = code.replace('`requests`', '`aiohttp`')
    code = code.replace('requests.request', 'aiohttp.request')

    code = DISCLAIMER + code
    with open(output_request_filename, 'w', encoding='UTF-8') as f:
        f.write(code)


def gen_client(output_client_filename: str) -> None:
    """Generate async version of client.py."""
    with open('yandex_music/client.py', 'r', encoding='UTF-8') as f:
        code = f.read()

    code = code.replace('Client', 'ClientAsync')
    code = code.replace(
        'from yandex_music.utils.request import Request', 'from yandex_music.utils.request_async import Request'
    )

    code = code.replace('def wrapper', 'async def wrapper')
    code = code.replace('result = method(', 'result = await method(')
    code = code.replace('@log\n    def', '@log\n    async def')
    code = code.replace('self.account_status', 'await self.account_status')

    for method in REQUEST_METHODS:
        code = code.replace(f'self._request.{method}', f'await self._request.{method}')
    for method in ('_like_action', '_dislike_action', '_get_list', '_get_likes'):
        code = code.replace(f'def {method}', f'async def {method}')
        code = code.replace(f'self.{method}(', f'await self.{method}(')

    # specific cases
    code = code.replace('self.users_playlists_change(', 'await self.users_playlists_change(')
    code = code.replace('self.rotor_station_feedback(', 'await self.rotor_station_feedback(')
    code = code.replace('return DownloadInfo.de_list', 'return await DownloadInfo.de_list_async')

    code = DISCLAIMER + code
    with open(output_client_filename, 'w', encoding='UTF-8') as f:
        f.write(code)


if __name__ == '__main__':
    request_filename = 'yandex_music/utils/request_async.py'
    client_filename = 'yandex_music/client_async.py'
    gen_request(request_filename)
    gen_client(client_filename)

    for file in (request_filename, client_filename):
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
        subprocess.run(['ruff', '--quiet', '--fix', file])  # noqa: S603, S607
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
