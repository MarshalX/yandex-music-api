"""Генерация документации клиентов на основе списка миксинов.

Сканирует директории _client/ и _client_async/ и дописывает в
client.md и client_async.md актуальный список миксинов.
Также обновляет заголовки в сгенерированных RST-файлах миксинов.

Маркер <!-- generated-mixins --> в md-файлах отделяет ручной контент
от автоматически генерируемого списка миксинов.
"""

import inspect
import json
import re
import sys
from pathlib import Path

DOCS_SOURCE = Path(__file__).parent / 'source'
YANDEX_MUSIC = Path(__file__).parent.parent / 'yandex_music'

sys.path.insert(0, str(YANDEX_MUSIC.parent))

MARKER = '<!-- generated-mixins -->'

TOCTREE_TEMPLATE = """\
## Миксины

```{{eval-rst}}
.. toctree::
   :maxdepth: 1

{toctree}
```
"""


def extract_mixin_title(module_path: Path) -> str:
    """Извлечь заголовок из первой строки docstring класса Mixin.

    Ожидаемый формат docstring:
        class FooMixin:
            \"\"\"Заголовок.

            Описание.
            \"\"\"

    Возвращает первую строку без завершающей точки.
    Если не удалось извлечь — возвращает имя файла в Title Case.
    """
    content = module_path.read_text()
    match = re.search(r'class \w+Mixin\([^)]*\):\s*"""(.+?)[\.]?\s*$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return module_path.stem.replace('_', ' ').title()


def get_mixin_modules(package_dir: Path) -> list[str]:
    """Получить отсортированный список модулей миксинов из директории пакета."""
    modules = []
    for f in sorted(package_dir.iterdir()):
        if f.suffix == '.py' and f.stem != '__init__':
            modules.append(f.stem)
    return modules


def fix_mixin_rst(package_name: str, modules: list[str]) -> None:
    """Обновить RST-файлы миксинов: читаемые заголовки, скрыть наследование."""
    # Заголовки берём из async-миксинов (они — источник истины)
    async_package = '_client_async'
    for module in modules:
        rst_file = DOCS_SOURCE / f'yandex_music.{package_name}.{module}.rst'
        if not rst_file.exists():
            continue

        content = rst_file.read_text()
        title = extract_mixin_title(YANDEX_MUSIC / async_package / f'{module}.py')

        # Заменить заголовок на читаемый
        content = re.sub(
            r'^.+\n=+\n',
            f'{title}\n{"=" * len(title)}\n',
            content,
            count=1,
        )

        # Скрыть "Bases: ClientBase" — детали реализации
        content = content.replace('   :show-inheritance:\n', '')

        rst_file.write_text(content)


def fix_utils_request_rst() -> None:
    """Исключить re-export'ы из yandex_music.utils.request.rst — их каноническая локация в request_base."""
    rst_file = DOCS_SOURCE / 'yandex_music.utils.request.rst'
    if not rst_file.exists():
        return

    content = rst_file.read_text()
    reexports = 'DefaultTimeout, DEFAULT_TIMEOUT, HEADERS, USER_AGENT, TimeoutType, default_timeout, RequestBase'
    content = content.replace(
        '   :members:\n',
        f'   :members:\n   :exclude-members: {reexports}\n',
        1,
    )
    rst_file.write_text(content)


def fix_yandex_music_rst() -> None:
    """Убрать приватные пакеты из yandex_music.rst и пустой automodule — он дублирует module.md."""
    rst_file = DOCS_SOURCE / 'yandex_music.rst'
    if not rst_file.exists():
        return

    content = rst_file.read_text()

    stripped_entries = (
        '   yandex_music._client\n',
        '   yandex_music._client_async\n',
        '   yandex_music._client_base\n',
        '   yandex_music.client\n',
        '   yandex_music.client_async\n',
    )
    for entry in stripped_entries:
        content = content.replace(entry, '')

    # Убрать '.. automodule:: yandex_music' без опций — module.md делает то же через include.
    content = content.replace('.. automodule:: yandex_music\n\n', '')

    rst_file.write_text(content)


# Файлы, которые apidoc всегда генерирует, но они не нужны в навигации.
# Содержимое миксинов и клиентов доступно через client.md/client_async.md напрямую.
FIXED_ORPHANS = (
    'modules.rst',
    'yandex_music._client.rst',
    'yandex_music._client_async.rst',
    'yandex_music._client_base.rst',
    'yandex_music.client.rst',
    'yandex_music.client_async.rst',
)


def _rst_module_path_exists(rst_stem: str) -> bool:
    """Проверить, существует ли модуль, соответствующий rst-файлу.

    yandex_music.album.label.rst -> yandex_music/album/label.py или yandex_music/album/label/__init__.py
    """
    parts = rst_stem.split('.')
    if parts[0] != 'yandex_music':
        return True  # не наш файл, не трогаем
    base = YANDEX_MUSIC.parent
    py_file = base / Path(*parts).with_suffix('.py')
    pkg_file = base / Path(*parts) / '__init__.py'
    return py_file.exists() or pkg_file.exists()


def remove_stale_rst() -> None:
    """Удалить устаревшие .rst-файлы, которые apidoc оставил после изменений в исходниках."""
    for name in FIXED_ORPHANS:
        (DOCS_SOURCE / name).unlink(missing_ok=True)

    for rst_file in DOCS_SOURCE.glob('yandex_music.*.rst'):
        stem = rst_file.stem
        if not _rst_module_path_exists(stem):
            rst_file.unlink()


def update_client_md(md_file: Path, package_name: str, modules: list[str]) -> None:
    """Обновить md-файл клиента: заменить всё после маркера на актуальный список миксинов."""
    content = md_file.read_text()

    if MARKER not in content:
        raise ValueError(f'Маркер {MARKER!r} не найден в {md_file}')

    header = content.split(MARKER)[0] + MARKER + '\n\n'
    toctree = '\n'.join(f'   yandex_music.{package_name}.{m}' for m in modules)
    md_file.write_text(header + TOCTREE_TEMPLATE.format(toctree=toctree))


def generate_redirects_map() -> None:
    """Записать карту коротких путей в _static/redirects_map.js.

    Для каждого публичного класса в yandex_music/__init__.py регистрирует маппинг
    yandex_music.X (старый anchor) → yandex_music.<pkg>.<mod>.html#yandex_music.<pkg>.<mod>.X.
    Используется клиентским JS-шимом redirects.js.
    """
    import yandex_music

    mapping: dict[str, str] = {}
    for name in dir(yandex_music):
        if name.startswith('_'):
            continue
        obj = getattr(yandex_music, name, None)
        if obj is None or not inspect.isclass(obj):
            continue
        module = inspect.getmodule(obj)
        if module is None or module.__name__ == 'yandex_music':
            continue
        canonical_page = module.__name__ + '.html'
        anchor = f'{module.__name__}.{obj.__name__}'
        mapping[f'yandex_music.{obj.__name__}'] = f'{canonical_page}#{anchor}'

    out = DOCS_SOURCE / '_static' / 'redirects_map.js'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        'window.__YM_REDIRECTS__ = ' + json.dumps(mapping, ensure_ascii=False, indent=2) + ';\n'
    )


def generate() -> None:
    """Генерация списков миксинов в client.md и client_async.md."""
    async_modules = get_mixin_modules(YANDEX_MUSIC / '_client_async')
    sync_modules = get_mixin_modules(YANDEX_MUSIC / '_client')

    remove_stale_rst()

    update_client_md(DOCS_SOURCE / 'client.md', '_client', sync_modules)
    update_client_md(DOCS_SOURCE / 'client_async.md', '_client_async', async_modules)

    fix_mixin_rst('_client_async', async_modules)
    fix_mixin_rst('_client', sync_modules)
    fix_yandex_music_rst()
    fix_utils_request_rst()
    generate_redirects_map()

    print(f'Сгенерировано client.md ({len(sync_modules)} миксинов)')
    print(f'Сгенерировано client_async.md ({len(async_modules)} миксинов)')


if __name__ == '__main__':
    generate()
