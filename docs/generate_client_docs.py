"""Генерация документации клиентов на основе списка миксинов.

Сканирует директории _client/ и _client_async/ и дописывает в
client.md и client_async.md актуальный список миксинов.
Также обновляет заголовки в сгенерированных RST-файлах миксинов.

Маркер <!-- generated-mixins --> в md-файлах отделяет ручной контент
от автоматически генерируемого списка миксинов.
"""

import re
from pathlib import Path

DOCS_SOURCE = Path(__file__).parent / 'source'
YANDEX_MUSIC = Path(__file__).parent.parent / 'yandex_music'

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


def fix_yandex_music_rst() -> None:
    """Убрать приватные пакеты из yandex_music.rst — они доступны через страницы клиентов."""
    rst_file = DOCS_SOURCE / 'yandex_music.rst'
    if not rst_file.exists():
        return

    content = rst_file.read_text()

    for entry in ('   yandex_music._client\n', '   yandex_music._client_async\n', '   yandex_music._client_base\n'):
        content = content.replace(entry, '')

    rst_file.write_text(content)


def update_client_md(md_file: Path, package_name: str, modules: list[str]) -> None:
    """Обновить md-файл клиента: заменить всё после маркера на актуальный список миксинов."""
    content = md_file.read_text()

    if MARKER not in content:
        raise ValueError(f'Маркер {MARKER!r} не найден в {md_file}')

    header = content.split(MARKER)[0] + MARKER + '\n\n'
    toctree = '\n'.join(f'   yandex_music.{package_name}.{m}' for m in modules)
    md_file.write_text(header + TOCTREE_TEMPLATE.format(toctree=toctree))


def generate() -> None:
    """Генерация списков миксинов в client.md и client_async.md."""
    async_modules = get_mixin_modules(YANDEX_MUSIC / '_client_async')
    sync_modules = get_mixin_modules(YANDEX_MUSIC / '_client')

    update_client_md(DOCS_SOURCE / 'client.md', '_client', sync_modules)
    update_client_md(DOCS_SOURCE / 'client_async.md', '_client_async', async_modules)

    fix_mixin_rst('_client_async', async_modules)
    fix_mixin_rst('_client', sync_modules)
    fix_yandex_music_rst()

    print(f'Сгенерировано client.md ({len(sync_modules)} миксинов)')
    print(f'Сгенерировано client_async.md ({len(async_modules)} миксинов)')


if __name__ == '__main__':
    generate()
