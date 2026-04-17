"""Генерация документации клиентов на основе списка миксинов.

Сканирует директории _client/ и _client_async/ и дописывает в
client.md и client_async.md актуальный список миксинов.
Также обновляет заголовки в сгенерированных RST-файлах миксинов.

Маркер <!-- generated-methods --> в md-файлах отделяет ручной контент
от автоматически генерируемого списка миксинов.
"""

import inspect
import json
import re
import sys
from pathlib import Path
from typing import Optional

DOCS_SOURCE = Path(__file__).parent / 'source'
YANDEX_MUSIC = Path(__file__).parent.parent / 'yandex_music'

sys.path.insert(0, str(YANDEX_MUSIC.parent))

MARKER = '<!-- generated-methods -->'

SECTION_TEMPLATE = """\
## Методы

```{{eval-rst}}
.. grid:: 2
   :gutter: 2

{cards}
```

```{{eval-rst}}
.. toctree::
   :hidden:
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


def _package_docstring_first_line(package_name: str) -> Optional[str]:
    """Прочитать первую строку module-docstring пакета yandex_music.<package_name>.

    Возвращает строку без завершающей точки, либо None, если docstring отсутствует.
    """
    import importlib

    try:
        module = importlib.import_module(f'yandex_music.{package_name}')
    except ImportError:
        return None
    doc = module.__doc__
    if not doc:
        return None
    first_line = doc.strip().splitlines()[0].strip()
    if first_line.endswith('.'):
        first_line = first_line[:-1]
    return first_line or None


def fix_package_headings() -> None:
    """Заменить заголовки подпакетных rst-файлов на русские имена из docstring'ов.

    Для каждого yandex_music.<pkg>.rst (без дополнительных точек в имени файла) —
    если в пакете есть module-docstring, берём первую строку и ставим её как
    заголовок страницы. Иначе не трогаем (остаётся apidoc-дефолт).
    """
    for rst_file in sorted(DOCS_SOURCE.glob('yandex_music.*.rst')):
        parts = rst_file.stem.split('.')
        # только подпакеты: yandex_music.<pkg>.rst (2 части)
        if len(parts) != 2 or parts[0] != 'yandex_music':
            continue
        pkg_name = parts[1]
        # проверяем, что это пакет (есть директория), а не одиночный модуль
        if not (YANDEX_MUSIC / pkg_name).is_dir():
            continue
        heading = _package_docstring_first_line(pkg_name)
        if not heading:
            continue
        content = rst_file.read_text()
        content = re.sub(
            r'^.+\n=+\n',
            f'{heading}\n{"=" * len(heading)}\n',
            content,
            count=1,
        )
        rst_file.write_text(content)


def _module_heading(module_path: str) -> Optional[str]:
    """Определить заголовок для rst-страницы модуля по лестнице правил.

    1. module-docstring (первая строка) — если есть, возвращаем её.
    2. Один публичный класс в модуле — возвращаем его имя.
    3. Несколько публичных классов — возвращаем PascalCase последнего компонента.
    4. Нет классов и нет docstring — None (апидок-дефолт оставляем).
    """
    import importlib

    try:
        module = importlib.import_module(module_path)
    except ImportError:
        return None
    # Правило 1: module-docstring
    doc = module.__doc__
    if doc:
        first_line = doc.strip().splitlines()[0].strip()
        if first_line.endswith('.'):
            first_line = first_line[:-1]
        if first_line:
            return first_line
    # Правила 2 и 3: классы
    public_classes = [
        name
        for name, obj in inspect.getmembers(module, inspect.isclass)
        if not name.startswith('_') and getattr(obj, '__module__', None) == module.__name__
    ]
    if len(public_classes) == 1:
        return public_classes[0]
    if len(public_classes) > 1:
        last_component = module_path.rsplit('.', 1)[-1]
        return ''.join(part.capitalize() for part in last_component.split('_'))
    return None


def _rst_is_module(rst_stem: str) -> bool:
    """Проверить, что rst-файл соответствует модулю (.py), а не пакету (директория)."""
    parts = rst_stem.split('.')
    if parts[0] != 'yandex_music':
        return False
    base = YANDEX_MUSIC.parent
    py_file = base / Path(*parts).with_suffix('.py')
    pkg_dir = base / Path(*parts)
    return py_file.exists() and not pkg_dir.is_dir()


def fix_module_headings() -> None:
    """Заменить заголовки rst-страниц модулей по лестнице правил из _module_heading.

    Обрабатывает все yandex_music.*.rst, соответствующие .py-файлам (не директориям).
    Пропускает приватные модули (_client/_client_async/_client_base) — они уже
    удалены remove_stale_rst или обрабатываются fix_mixin_rst.
    """
    for rst_file in sorted(DOCS_SOURCE.glob('yandex_music.*.rst')):
        stem = rst_file.stem
        if not _rst_is_module(stem):
            continue
        # Пропустить миксины — у них свой fix_mixin_rst
        if '._client.' in stem or '._client_async.' in stem:
            continue
        heading = _module_heading(stem)
        if not heading:
            continue
        content = rst_file.read_text()
        content = re.sub(
            r'^.+\n=+\n',
            f'{heading}\n{"=" * len(heading)}\n',
            content,
            count=1,
        )
        rst_file.write_text(content)


MODELS_MARKER = '<!-- generated-models-toctree -->'

# Пакеты/модули, которые на самостоятельных caption'ах в сайдбаре (не в «Модели»).
MODELS_EXCLUDED = {'exceptions', 'utils', 'base'}


def _discover_public_modules() -> tuple[list[str], list[str]]:
    """Вернуть (packages, single_modules) публичной поверхности yandex_music.

    packages — директории с __init__.py (без приватных _*, без исключённых).
    single_modules — .py-файлы в корне пакета (без приватных и исключённых).
    """
    packages = []
    single_modules = []
    for entry in sorted(YANDEX_MUSIC.iterdir()):
        name = entry.name
        if name.startswith('_') or name == '__pycache__':
            continue
        if entry.is_dir():
            if name in MODELS_EXCLUDED:
                continue
            if (entry / '__init__.py').exists():
                packages.append(name)
        elif entry.is_file() and entry.suffix == '.py':
            stem = entry.stem
            if stem == '__init__':
                continue
            if stem in MODELS_EXCLUDED:
                continue
            # Исключить client/client_async.py — они не модели и в сайдбаре отдельно.
            if stem in ('client', 'client_async'):
                continue
            single_modules.append(stem)
    return packages, single_modules


def build_models_toctree() -> None:
    """Записать скрытый toctree в models.md между маркером и концом файла.

    Также печатает предупреждение о подпакетах/модулях, которые не упомянуты
    в карточках models.md (детектим по наличию строки ':link: yandex_music.<name>' в файле).
    """
    models_md = DOCS_SOURCE / 'models.md'
    if not models_md.exists():
        return

    packages, single_modules = _discover_public_modules()
    all_docnames = [f'yandex_music.{p}' for p in packages] + [f'yandex_music.{m}' for m in single_modules]

    content = models_md.read_text()
    if MODELS_MARKER not in content:
        raise ValueError(f'Маркер {MODELS_MARKER!r} не найден в {models_md}')

    head = content.split(MODELS_MARKER)[0] + MODELS_MARKER + '\n\n'
    toctree_lines = '\n'.join(f'   {d}' for d in all_docnames)
    block = f'```{{eval-rst}}\n.. toctree::\n   :hidden:\n   :maxdepth: 2\n\n{toctree_lines}\n```\n'
    models_md.write_text(head + block)

    # Sanity-check: предупредим про непокрытые карточками подпакеты/модули.
    missing = [d for d in all_docnames if f':link: {d}' not in head]
    if missing:
        print('ВНИМАНИЕ: в models.md нет карточки для:', ', '.join(missing))


def fix_utils_request_rst() -> None:
    """Исключить re-export'ы из yandex_music.utils.request.rst — их каноническая локация в request_base."""
    rst_file = DOCS_SOURCE / 'yandex_music.utils.request.rst'
    if not rst_file.exists():
        return

    content = rst_file.read_text()
    if ':exclude-members:' in content:
        return
    reexports = 'DefaultTimeout, DEFAULT_TIMEOUT, HEADERS, USER_AGENT, TimeoutType, default_timeout, RequestBase'
    content = content.replace(
        '   :members:\n',
        f'   :members:\n   :exclude-members: {reexports}\n',
        1,
    )
    rst_file.write_text(content)


def fix_yandex_music_rst() -> None:
    """Убрать приватные пакеты из yandex_music.rst и сделать его orphan.

    Страница yandex_music нужна для canonical-алиасов (register_short_aliases),
    но в навигации не показывается — редирект на models.html через page-карту.
    """
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

    content = content.replace('.. automodule:: yandex_music\n\n', '')

    if not content.startswith(':orphan:'):
        content = ':orphan:\n\n' + content

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


def _mixin_method_names(package_name: str, module: str) -> list[str]:
    """Получить список публичных методов миксина через интроспекцию класса."""
    import importlib

    mod = importlib.import_module(f'yandex_music.{package_name}.{module}')
    mixin_cls = next(
        (
            obj
            for name, obj in inspect.getmembers(mod, inspect.isclass)
            if name.endswith('Mixin') and obj.__module__ == mod.__name__
        ),
        None,
    )
    if mixin_cls is None:
        return []
    return sorted(
        name
        for name, obj in mixin_cls.__dict__.items()
        if callable(obj)
        and not name.startswith('_')
        and not ('_' not in name and name != name.lower())  # skip camelCase aliases
    )


def _mixin_card(package_name: str, module: str) -> str:
    """Сгенерировать grid-item-card для миксина с названием и списком методов."""
    title = extract_mixin_title(YANDEX_MUSIC / '_client_async' / f'{module}.py')
    methods = _mixin_method_names(package_name, module)
    methods_line = ', '.join(f'``{m}``' for m in methods) if methods else '—'
    return (
        f'   .. grid-item-card:: {title}\n'
        f'      :link: yandex_music.{package_name}.{module}\n'
        f'      :link-type: doc\n'
        f'\n'
        f'      {methods_line}\n'
    )


def update_client_md(md_file: Path, package_name: str, modules: list[str]) -> None:
    """Обновить md-файл клиента: заменить всё после маркера на карточки миксинов + скрытый toctree."""
    content = md_file.read_text()

    if MARKER not in content:
        raise ValueError(f'Маркер {MARKER!r} не найден в {md_file}')

    header = content.split(MARKER)[0] + MARKER + '\n\n'
    cards = '\n'.join(_mixin_card(package_name, m) for m in modules)
    toctree = '\n'.join(f'   yandex_music.{package_name}.{m}' for m in modules)
    md_file.write_text(header + SECTION_TEMPLATE.format(cards=cards, toctree=toctree))


def generate_redirects_map() -> None:
    """Записать карту редиректов в _static/redirects_map.js.

    Пишет два объекта:
      - window.__YM_REDIRECTS__: якорные алиасы yandex_music.X → dedicated-страница.
      - window.__YM_PAGE_REDIRECTS__: page-level редиректы для удалённых страниц.
    """
    import yandex_music

    anchor_map: dict[str, str] = {}
    for name in dir(yandex_music):
        if name.startswith('_'):
            continue
        obj = getattr(yandex_music, name, None)
        if obj is None or not inspect.isclass(obj):
            continue
        module = inspect.getmodule(obj)
        if module is None or module.__name__ == 'yandex_music':
            continue
        canonical_page = module.__name__
        anchor = f'{module.__name__}.{obj.__name__}'
        anchor_map[f'yandex_music.{obj.__name__}'] = f'{canonical_page}#{anchor}'

    page_map: dict[str, str] = {
        'module.html': 'models.html',
        'yandex_music.html': 'models.html',
    }

    out = DOCS_SOURCE / '_static' / 'redirects_map.js'
    out.parent.mkdir(parents=True, exist_ok=True)
    body = (
        'window.__YM_REDIRECTS__ = ' + json.dumps(anchor_map, ensure_ascii=False, indent=2) + ';\n'
        'window.__YM_PAGE_REDIRECTS__ = ' + json.dumps(page_map, ensure_ascii=False, indent=2) + ';\n'
    )
    out.write_text(body)


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
    fix_package_headings()
    fix_module_headings()
    build_models_toctree()
    fix_utils_request_rst()
    generate_redirects_map()

    print(f'Сгенерировано client.md ({len(sync_modules)} миксинов)')
    print(f'Сгенерировано client_async.md ({len(async_modules)} миксинов)')


if __name__ == '__main__':
    generate()
