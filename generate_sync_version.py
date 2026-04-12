#!/usr/bin/env python3
"""Generate sync version of client_async.py using unasync."""

import os
import shutil
import subprocess
import tempfile

import unasync

DISCLAIMER = "# THIS IS AUTO GENERATED COPY OF client_async.py. DON'T EDIT IT BY HANDS #"
DISCLAIMER = f'{"#" * len(DISCLAIMER)}\n{DISCLAIMER}\n{"#" * len(DISCLAIMER)}\n\n'

SRC = 'yandex_music/client_async.py'
DST = 'yandex_music/client.py'

ADDITIONAL_REPLACEMENTS = {
    'ClientAsync': 'Client',
    'request_async': 'request',
    'de_list_async': 'de_list',
}

# unasync operates on tokens, so replacements inside docstrings/comments
# are not handled. These are applied as plain string replacements after generation.
STRING_REPLACEMENTS = {
    'ClientAsync': 'Client',
}


def gen_client() -> None:
    """Generate sync version of client_async.py."""
    with tempfile.TemporaryDirectory() as tmp:
        # unasync is directory-based: it replaces fromdir with todir in file paths.
        # Set up a temp structure: tmp/_async/client.py -> tmp/_sync/client.py
        async_dir = os.path.join(tmp, '_async')
        sync_dir = os.path.join(tmp, '_sync')
        os.makedirs(async_dir)

        shutil.copy2(SRC, os.path.join(async_dir, 'client.py'))

        rules = [
            unasync.Rule(
                fromdir=async_dir,
                todir=sync_dir,
                additional_replacements=ADDITIONAL_REPLACEMENTS,
            ),
        ]

        unasync.unasync_files(
            [os.path.join(async_dir, 'client.py')],
            rules,
        )

        generated = os.path.join(sync_dir, 'client.py')
        with open(generated, 'r', encoding='UTF-8') as f:
            code = f.read()

    # Apply string-level replacements for things unasync misses (e.g. inside docstrings).
    for old, new in STRING_REPLACEMENTS.items():
        code = code.replace(old, new)

    code = DISCLAIMER + code
    with open(DST, 'w', encoding='UTF-8') as f:
        f.write(code)


if __name__ == '__main__':
    gen_client()

    for file in (DST,):
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
        subprocess.run(['ruff', 'check', '--quiet', '--fix', file])  # noqa: S603, S607
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
