"""Generate sync version of async client code using unasync."""

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

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
    # Blanket asyncio->time: currently only `asyncio.sleep` is used in _client_async/.
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


def _run_unasync(
    src_files: List[str],
    src_dir: str,
    dst_dir: str,
    extra_replacements: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Run unasync on source files and return mapping of dst_path -> generated code."""
    results: Dict[str, str] = {}

    with tempfile.TemporaryDirectory() as tmp:
        async_dir = Path(tmp, '_async')
        sync_dir = Path(tmp, '_sync')
        async_dir.mkdir(parents=True)

        for src_file in src_files:
            tmp_src = async_dir / Path(src_file).relative_to(src_dir)
            tmp_src.parent.mkdir(parents=True, exist_ok=True)
            _ = shutil.copy2(src_file, tmp_src)

        rules = [
            unasync.Rule(
                fromdir=str(async_dir),
                todir=str(sync_dir),
                additional_replacements={
                    **ADDITIONAL_REPLACEMENTS,
                    **(extra_replacements if extra_replacements is not None else {}),
                },
            ),
        ]

        tmp_files = [str(async_dir / Path(f).relative_to(src_dir)) for f in src_files]
        unasync.unasync_files(tmp_files, rules)

        for src_file in src_files:
            rel_path = Path(src_file).relative_to(src_dir)
            code = (sync_dir / rel_path).read_text(encoding='UTF-8')

            for old, new in STRING_REPLACEMENTS.items():
                code = code.replace(old, new)

            results[(Path(dst_dir) / rel_path).as_posix()] = code

    return results


def gen_client() -> List[str]:
    """Generate sync version of all async client files."""
    generated_files: List[str] = []

    # Generate sync client.py from client_async.py
    client_results = _run_unasync(
        [CLIENT_SRC],
        Path(CLIENT_SRC).parent.as_posix(),
        Path(CLIENT_DST).parent.as_posix(),
    )
    ((_, code),) = client_results.items()
    disclaimer = _make_disclaimer(CLIENT_SRC)
    _ = Path(CLIENT_DST).write_text(disclaimer + code, encoding='UTF-8')
    generated_files.append(CLIENT_DST)

    # Generate sync mixin files from _client_async/ to _client/
    mixin_files = sorted(p.as_posix() for p in Path(MIXINS_SRC_DIR).glob('*.py'))
    if len(mixin_files) > 0:
        mixin_results = _run_unasync(mixin_files, MIXINS_SRC_DIR, MIXINS_DST_DIR)
        Path(MIXINS_DST_DIR).mkdir(parents=True, exist_ok=True)

        for dst_path, code in mixin_results.items():
            src_rel = (Path(MIXINS_SRC_DIR) / Path(dst_path).relative_to(MIXINS_DST_DIR)).as_posix()
            disclaimer = _make_disclaimer(src_rel)
            _ = Path(dst_path).write_text(disclaimer + code, encoding='UTF-8')
            generated_files.append(dst_path)

    # Generate sync ynison.simple from ynison.simple_async
    ynison_results = _run_unasync(
        [YNISON_SIMPLE_SRC],
        Path(YNISON_SIMPLE_SRC).parent.as_posix(),
        Path(YNISON_SIMPLE_DST).parent.as_posix(),
        # только для ynison, чтобы не задеть основной клиент
        extra_replacements={'client_async': 'client'},
    )
    ((_, code),) = ynison_results.items()
    disclaimer = _make_disclaimer(YNISON_SIMPLE_SRC)
    _ = Path(YNISON_SIMPLE_DST).write_text(disclaimer + code, encoding='UTF-8')
    generated_files.append(YNISON_SIMPLE_DST)

    return generated_files


if __name__ == '__main__':
    files = gen_client()

    for file in files:
        _ = subprocess.run(['ruff', 'format', '--quiet', file], check=False)  # noqa: S603, S607
        _ = subprocess.run(['ruff', 'check', '--quiet', '--fix', file], check=False)  # noqa: S603, S607
        _ = subprocess.run(['ruff', 'format', '--quiet', file], check=False)  # noqa: S603, S607
