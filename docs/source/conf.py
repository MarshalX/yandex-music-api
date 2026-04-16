"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
http://www.sphinx-doc.org/en/master/config

-- Path setup --------------------------------------------------------------

If extensions (or modules to document with autodoc) are in another directory,
add these directories to sys.path here. If the directory is relative to the
documentation root, use os.path.abspath to make it absolute, like shown here.
"""

import inspect
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

master_doc = 'index'

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Project information -----------------------------------------------------

project = 'Yandex Music API'
copyright = '2019-2026 Ilya (Marshal) <https://github.com/MarshalX>'
author = 'Ilya (Marshal)'

language = 'en'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx_copybutton', 'myst_parser']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'modules.rst',
    'yandex_music._client.rst',
    'yandex_music._client_async.rst',
    'yandex_music._client_base.rst',
    'yandex_music.client.rst',
    'yandex_music.client_async.rst',
]

# myst

myst_heading_anchors = 4
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html?highlight=header-anchors#code-fences-using-colons
myst_enable_extensions = ['colon_fence']
# README.md начинается с H2 — нормально для GitHub, но MyST предупреждает. Глушим.
suppress_warnings = ['myst.header', 'ref.python']
# TODO add substitution https://myst-parser.readthedocs.io/en/latest/syntax/optional.html?highlight=header-anchors#substitutions-with-jinja2

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# These folders are copied to the documentation's HTML output
html_static_path = ['_static']

html_search_language = 'ru'

html_title = 'Yandex Music API'
html_theme = 'furo'

html_css_files = [
    'css/custom.css',
]

html_js_files = [
    'redirects_map.js',
    'redirects.js',
]

html_theme_options = {
    'navigation_with_keys': True,
}


def _is_camel_case(name: str) -> bool:
    """Проверяет, является ли имя camelCase (не snake_case и не UPPER_CASE)."""
    return name != name.lower() and '_' not in name and not name.startswith('_')


def autodoc_skip_member(_app, what, name, _obj, skip, _options) -> bool:  # noqa: ANN001
    """Скрыть camelCase псевдонимы из документации."""
    if not skip and what == 'class' and _is_camel_case(name):
        return True
    return skip


def register_short_aliases(_app, env) -> None:  # noqa: ANN001
    """Зарегистрировать короткие пути вида yandex_music.X как алиасы канонических."""
    import yandex_music

    py_objects = env.domains['py'].objects
    for name in dir(yandex_music):
        if name.startswith('_'):
            continue
        obj = getattr(yandex_music, name, None)
        if obj is None or not inspect.isclass(obj):
            continue
        module = inspect.getmodule(obj)
        if module is None or module.__name__ == 'yandex_music':
            continue
        canonical = f'{module.__name__}.{obj.__name__}'
        short = f'yandex_music.{obj.__name__}'
        if canonical in py_objects and short not in py_objects:
            entry = py_objects[canonical]
            py_objects[short] = entry.__class__(entry.docname, entry.node_id, entry.objtype, aliased=True)


def setup(app) -> None:  # noqa: ANN001
    """Настройка Sphinx-приложения."""
    app.connect('autodoc-skip-member', autodoc_skip_member)
    app.connect('env-check-consistency', register_short_aliases)
