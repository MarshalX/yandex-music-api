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

from sphinxawesome_theme.postprocess import Icons

sys.path.insert(0, os.path.abspath('../..'))

master_doc = 'index'

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Project information -----------------------------------------------------

project = 'Yandex Music API'
copyright = '2019-2026 Ilya (Marshal).'
author = 'Ilya (Marshal)'

language = 'en'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinxext.opengraph',
    'sphinx_design',
    'sphinx_sitemap',
    'myst_parser',
]

DOCSEARCH_APP_ID = os.environ.get('DOCSEARCH_APP_ID')
DOCSEARCH_API_KEY = os.environ.get('DOCSEARCH_API_KEY')
DOCSEARCH_INDEX_NAME = os.environ.get('DOCSEARCH_INDEX_NAME')

if DOCSEARCH_APP_ID and DOCSEARCH_API_KEY and DOCSEARCH_INDEX_NAME:
    extensions.append('sphinx_docsearch')
    docsearch_app_id = DOCSEARCH_APP_ID
    docsearch_api_key = DOCSEARCH_API_KEY
    docsearch_index_name = DOCSEARCH_INDEX_NAME

    docsearch_placeholder = 'Поиск по документации'
    docsearch_missing_results_url = (
        'https://github.com/MarshalX/yandex-music-api/discussions/new?category=q-a&title=${query}'
    )
else:
    print(  # noqa: T201
        '[conf.py] DocSearch env vars missing — built-in Sphinx search will be used',
        file=sys.stderr,
    )

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

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
myst_enable_extensions = ['colon_fence', 'deflist']
# README.md начинается с H2 — нормально для GitHub, но MyST предупреждает. Глушим.
suppress_warnings = ['myst.header', 'ref.python']
# TODO add substitution https://myst-parser.readthedocs.io/en/latest/syntax/optional.html?highlight=header-anchors#substitutions-with-jinja2

# pygments
pygments_style = 'friendly'
pygments_style_dark = 'monokai'

# sitemap
sitemap_locales = [None]
sitemap_url_scheme = '{link}'

# OpenGraph
ogp_site_url = 'https://ym.marshal.dev/'
ogp_image = 'https://repository-images.githubusercontent.com/185270983/20525f14-1a05-4ecf-bffa-074382dc423c'
ogp_type = 'article'
ogp_enable_meta_description = True

# autodoc options
autodoc_default_options = {
    'members': True,
    # show-inheritance намеренно убран — Bases: шумит на каждой модели
}
autodoc_member_order = 'bysource'
autodoc_typehints = 'none'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# These folders are copied to the documentation's HTML output
html_static_path = ['_static']
html_title = project
html_baseurl = 'https://ym.marshal.dev/'
html_favicon = '_static/img/favicon-128x128.png'
html_extra_path = ['robots.txt']
html_theme = 'sphinxawesome_theme'
html_domain_indices = False
html_copy_source = False
html_show_sourcelink = False
html_search_language = 'ru'
html_permalinks_icon = Icons.permalinks_icon

html_css_files = [
    'css/custom.css',
]

html_js_files = [
    'redirects_map.js',
    'redirects.js',
]

html_theme_options = {
    'show_prev_next': True,
    'awesome_external_links': True,
    'show_breadcrumbs': True,
    'show_scrolltop': True,
    'main_nav_links': {
        'Начало': 'readme',
        'Примеры': 'examples',
        'Клиент': 'client',
        'Глоссарий': 'glossary',
        'Список изменений': 'changes',
    },
    'logo_light': '_static/img/logo.png',
    'logo_dark': '_static/img/logo.png',
    'extra_header_link_icons': {
        'репозиторий на GitHub': {
            'link': 'https://github.com/MarshalX/yandex-music-api',
            'icon': (
                '<svg height="16px" style="margin-top:-2px;display:inline" '
                'viewBox="0 0 45 44" '
                'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
                '<path fill-rule="evenodd" clip-rule="evenodd" '
                'd="M22.477.927C10.485.927.76 10.65.76 22.647c0 9.596 6.223 17.736 '
                '14.853 20.608 1.087.2 1.483-.47 1.483-1.047 '
                '0-.516-.019-1.881-.03-3.693-6.04 '
                '1.312-7.315-2.912-7.315-2.912-.988-2.51-2.412-3.178-2.412-3.178-1.972-1.346.149-1.32.149-1.32 '
                '2.18.154 3.327 2.24 3.327 2.24 1.937 3.318 5.084 2.36 6.321 '
                '1.803.197-1.403.759-2.36 '
                '1.379-2.903-4.823-.548-9.894-2.412-9.894-10.734 '
                '0-2.37.847-4.31 2.236-5.828-.224-.55-.969-2.759.214-5.748 0 0 '
                '1.822-.584 5.972 2.226 '
                '1.732-.482 3.59-.722 5.437-.732 1.845.01 3.703.25 5.437.732 '
                '4.147-2.81 5.967-2.226 '
                '5.967-2.226 1.185 2.99.44 5.198.217 5.748 1.392 1.517 2.232 3.457 '
                '2.232 5.828 0 '
                '8.344-5.078 10.18-9.916 10.717.779.67 1.474 1.996 1.474 4.021 0 '
                '2.904-.027 5.247-.027 '
                '5.96 0 .58.392 1.256 1.493 1.044C37.981 40.375 44.2 32.24 44.2 '
                '22.647c0-11.996-9.726-21.72-21.722-21.72" '
                'fill="currentColor"/></svg>'
            ),
        },
        'пакет на PyPI': {
            'link': 'https://pypi.org/project/yandex-music',
            'icon': (
                '<svg height="16px" style="margin-top:-2px;display:inline" '
                'viewBox="0 0 24 24" '
                'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
                '<path d="M11.885.002c-.98.004-1.918.088-2.744.234-2.433.43-2.875 1.33-2.875 '
                '2.99v2.193h5.75v.73H4.108c-1.672 0-3.136 1.005-3.594 2.917-.528 2.19-.552 '
                '3.558 0 5.846.41 '
                '1.703 1.386 2.916 3.058 2.916h1.977v-2.628c0-1.9 1.644-3.574 3.594-3.574h5.746c1.6 '
                '0 2.875-1.315 2.875-2.92V3.226c0-1.558-1.314-2.728-2.875-2.988A17.99 17.99 0 0 0 '
                '11.885.002zM8.775 1.762c.595 0 1.08.492 1.08 1.097 0 .603-.485 1.09-1.08 '
                '1.09-.596 0-1.08-.487-1.08-1.09-.001-.606.484-1.097 1.08-1.097z"/>'
                '<path d="M19.132 6.149v2.556c0 1.982-1.68 3.651-3.595 3.651H9.79c-1.574 '
                '0-2.876 1.347-2.876 '
                '2.922v5.478c0 1.56 1.356 2.475 2.876 2.922 1.822.535 3.567.632 5.747 0 '
                '1.447-.419 2.875-1.263 '
                '2.875-2.922v-2.193H12.67v-.73h8.617c1.672 0 2.295-1.165 2.876-2.917.6-1.804.575-3.54 '
                '0-5.846-.414-1.664-1.201-2.917-2.876-2.917h-2.156zm-3.232 13.876c.596 0 1.08.486 '
                '1.08 1.09 0 .606-.484 '
                '1.097-1.08 1.097-.595 0-1.08-.491-1.08-1.097.001-.604.485-1.09 1.08-1.09z"/></svg>'
            ),
        },
        'чат в Telegram': {
            'link': 'https://t.me/yandex_music_api',
            'icon': (
                '<svg height="16px" style="margin-top:-2px;display:inline" '
                'viewBox="0 0 24 24" '
                'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
                '<path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 '
                '0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 '
                '.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 '
                '8.627-.168.9-.499 1.201-.82 '
                '1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-'
                '1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 '
                '3.247-2.977 '
                '3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 '
                '1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252'
                '-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 '
                '3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>'
            ),
        },
    },
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
