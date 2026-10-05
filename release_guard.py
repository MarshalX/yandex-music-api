#!/usr/bin/env python3
"""Проверка версии перед релизом и подготовка текста GitHub-релиза. Используется в CI/CD.

Ожидает версию в переменной окружения VERSION и список git-тегов на stdin.
"""

import os
import re
import sys
from pathlib import Path

from packaging.version import InvalidVersion, Version

VERSION_RE = re.compile(r'\d+\.\d+\.\d+((a|b|rc)\d+)?')
INIT_VERSION_RE = re.compile(r"__version__ = '(.+)'")
DATE_RE = re.compile(r'\*\*\d{2}\.\d{2}\.\d{4}\*\*')

INIT_PATH = Path('yandex_music', '__init__.py')
CHANGES_PATH = Path('CHANGES.md')
NOTES_PATH = Path('RELEASE_NOTES.md')


def fail(message: str) -> None:
    """Вывести ошибку в формате аннотации GitHub Actions и завершить работу."""
    sys.stdout.write(f'::error::{message}\n')
    sys.exit(1)


def set_output(name: str, value: str) -> None:
    """Передать значение следующим шагам через $GITHUB_OUTPUT."""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if not github_output:
        return

    with open(github_output, 'a', encoding='UTF-8') as f:
        f.write(f'{name}={value}\n')


def parse_tags(lines: list) -> list:
    """Разобрать теги вида vX.Y.Z, пропуская не являющиеся версиями."""
    versions = []
    for line in lines:
        tag = line.strip()
        if not tag.startswith('v'):
            continue

        try:
            versions.append(Version(tag[1:]))
        except InvalidVersion:
            continue

    return versions


def find_section(changes: str, version: str) -> str:
    """Найти раздел ``## Версия X.Y.Z`` в CHANGES.md; пустая строка, если его нет."""
    marker = f'## Версия {version}\n'
    start = changes.find(marker)
    if start == -1:
        return ''

    end = changes.find('\n## Версия ', start + len(marker))
    if end == -1:
        end = len(changes)

    return changes[start + len(marker) : end].strip()


def build_notes(section: str) -> str:
    """Убрать строку с датой из раздела CHANGES.md."""
    lines = section.split('\n')
    if lines and DATE_RE.fullmatch(lines[0].strip()):
        lines = lines[1:]

    return '\n'.join(lines).strip() + '\n'


def main() -> None:
    """Проверить версию, тег, __version__ и CHANGES.md, записать RELEASE_NOTES.md."""
    raw = os.environ.get('VERSION', '').strip()
    if not VERSION_RE.fullmatch(raw):
        fail(f'"{raw}" не похоже на версию вида 3.1.0 или 3.1.0b3')

    version = Version(raw)

    released = parse_tags(sys.stdin.read().splitlines())
    if version in released:
        fail(f'Тег для {raw} уже существует, опубликованный релиз неизменяем')

    latest = max(released) if released else None
    if latest is not None and version < latest:
        fail(f'{raw} не новее последнего релиза {latest}')

    init_match = INIT_VERSION_RE.search(INIT_PATH.read_text(encoding='UTF-8'))
    init_version = init_match.group(1) if init_match else None
    if init_version != raw:
        fail(f'__version__ в {INIT_PATH} равен {init_version}, а выпускается {raw}')

    section = find_section(CHANGES_PATH.read_text(encoding='UTF-8'), version.base_version)
    if version.is_prerelease:
        notes = build_notes(section) if section else f'Предварительная версия {raw}.\n'
    else:
        if not section:
            fail(f'В {CHANGES_PATH} нет раздела "## Версия {raw}"')
        if not DATE_RE.fullmatch(section.split('\n')[0].strip()):
            fail(f'У раздела "## Версия {raw}" в {CHANGES_PATH} не проставлена дата вида **ДД.ММ.ГГГГ**')
        notes = build_notes(section)

    NOTES_PATH.write_text(notes, encoding='UTF-8')

    set_output('version', raw)
    set_output('prerelease', 'true' if version.is_prerelease else 'false')
    sys.stdout.write(f'Выпускается {raw} поверх {latest or "ничего"}\n')


if __name__ == '__main__':
    main()
