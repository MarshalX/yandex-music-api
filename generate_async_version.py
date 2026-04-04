#!/usr/bin/env python3
"""Generate async version of client.py."""

import subprocess

DISCLAIMER = "# THIS IS AUTO GENERATED COPY OF client.py. DON'T EDIT IN BY HANDS #"
DISCLAIMER = f'{"#" * len(DISCLAIMER)}\n{DISCLAIMER}\n{"#" * len(DISCLAIMER)}\n\n'

REQUEST_METHODS = ('_request_wrapper', 'get', 'post', 'retrieve', 'download')


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
    client_filename = 'yandex_music/client_async.py'
    gen_client(client_filename)

    for file in (client_filename,):
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
        subprocess.run(['ruff', '--quiet', '--fix', file])  # noqa: S603, S607
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
