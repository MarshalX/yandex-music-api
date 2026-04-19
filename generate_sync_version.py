#!/usr/bin/env python3
"""Generate sync version of async client code using unasync."""

import glob
import os
import shutil
import subprocess
import tempfile

import unasync

DISCLAIMER = "# THIS IS AUTO GENERATED COPY OF {source}. DON'T EDIT IT BY HANDS #"

CLIENT_SRC = 'yandex_music/client_async.py'
CLIENT_DST = 'yandex_music/client.py'

MIXINS_SRC_DIR = 'yandex_music/_client_async'
MIXINS_DST_DIR = 'yandex_music/_client'

YNISON_SIMPLE_SRC = 'yandex_music/ynison/simple_async.py'
YNISON_SIMPLE_DST = 'yandex_music/ynison/simple.py'

ADDITIONAL_REPLACEMENTS = {
    'ClientAsync': 'Client',
    'request_async': 'request',
    'de_list_async': 'de_list',
    '_client_async': '_client',
    'simple_async': 'simple',
    'YnisonClientAsync': 'YnisonClient',
    # Blanket asyncio->time — currently only `asyncio.sleep` is used in _client_async/.
    # Any future use of other asyncio primitives (gather, Lock, etc.) will be silently
    # rewritten to `time.*` and must be handled explicitly.
    'asyncio': 'time',
}

# unasync operates on tokens, so replacements inside docstrings/comments
# are not handled. These are applied as plain string replacements after generation.
STRING_REPLACEMENTS = {
    'ClientAsync': 'Client',
    'simple_async': 'simple',
    # Ynison simple_async → simple: заголовки и описания должны отличаться,
    # иначе sphinx рисует дубликаты пунктов в сайдбаре.
    'асинхронный интерфейс': 'интерфейс',
    'Каждая корутина': 'Каждая функция',
}


def _make_disclaimer(source: str) -> str:
    """Create a disclaimer header for a generated file."""
    text = DISCLAIMER.format(source=source)
    return f'{"#" * len(text)}\n{text}\n{"#" * len(text)}\n\n'


def _run_unasync(src_files: list[str], src_dir: str, dst_dir: str) -> dict[str, str]:
    """Run unasync on source files and return mapping of dst_path -> generated code."""
    results = {}

    with tempfile.TemporaryDirectory() as tmp:
        async_dir = os.path.join(tmp, '_async')
        sync_dir = os.path.join(tmp, '_sync')
        os.makedirs(async_dir)

        for src_file in src_files:
            rel_path = os.path.relpath(src_file, src_dir)
            tmp_src = os.path.join(async_dir, rel_path)
            os.makedirs(os.path.dirname(tmp_src), exist_ok=True)
            shutil.copy2(src_file, tmp_src)

        rules = [
            unasync.Rule(
                fromdir=async_dir,
                todir=sync_dir,
                additional_replacements=ADDITIONAL_REPLACEMENTS,
            ),
        ]

        tmp_files = [os.path.join(async_dir, os.path.relpath(f, src_dir)) for f in src_files]
        unasync.unasync_files(tmp_files, rules)

        for src_file in src_files:
            rel_path = os.path.relpath(src_file, src_dir)
            generated = os.path.join(sync_dir, rel_path)
            with open(generated, 'r', encoding='UTF-8') as f:
                code = f.read()

            for old, new in STRING_REPLACEMENTS.items():
                code = code.replace(old, new)

            results[os.path.join(dst_dir, rel_path)] = code

    return results


def gen_client() -> list[str]:
    """Generate sync version of all async client files."""
    generated_files = []

    # Generate sync client.py from client_async.py
    client_results = _run_unasync(
        [CLIENT_SRC],
        os.path.dirname(CLIENT_SRC),
        os.path.dirname(CLIENT_DST),
    )
    ((_, code),) = client_results.items()
    disclaimer = _make_disclaimer(CLIENT_SRC)
    with open(CLIENT_DST, 'w', encoding='UTF-8') as f:
        f.write(disclaimer + code)
    generated_files.append(CLIENT_DST)

    # Generate sync mixin files from _client_async/ to _client/
    mixin_files = sorted(glob.glob(os.path.join(MIXINS_SRC_DIR, '*.py')))
    if mixin_files:
        mixin_results = _run_unasync(mixin_files, MIXINS_SRC_DIR, MIXINS_DST_DIR)
        os.makedirs(MIXINS_DST_DIR, exist_ok=True)

        for dst_path, code in mixin_results.items():
            src_rel = os.path.relpath(
                os.path.join(MIXINS_SRC_DIR, os.path.relpath(dst_path, MIXINS_DST_DIR)),
            )
            disclaimer = _make_disclaimer(src_rel)
            with open(dst_path, 'w', encoding='UTF-8') as f:
                f.write(disclaimer + code)
            generated_files.append(dst_path)

    # Generate sync ynison.simple from ynison.simple_async
    ynison_results = _run_unasync(
        [YNISON_SIMPLE_SRC],
        os.path.dirname(YNISON_SIMPLE_SRC),
        os.path.dirname(YNISON_SIMPLE_DST),
    )
    ((_, code),) = ynison_results.items()
    disclaimer = _make_disclaimer(YNISON_SIMPLE_SRC)
    with open(YNISON_SIMPLE_DST, 'w', encoding='UTF-8') as f:
        f.write(disclaimer + code)
    generated_files.append(YNISON_SIMPLE_DST)

    return generated_files


if __name__ == '__main__':
    files = gen_client()

    for file in files:
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
        subprocess.run(['ruff', 'check', '--quiet', '--fix', file])  # noqa: S603, S607
        subprocess.run(['ruff', 'format', '--quiet', file])  # noqa: S603, S607
