"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
http://www.sphinx-doc.org/en/master/config

-- Path setup --------------------------------------------------------------

If extensions (or modules to document with autodoc) are in another directory,
add these directories to sys.path here. If the directory is relative to the
documentation root, use os.path.abspath to make it absolute, like shown here.
"""
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
copyright = '2019-2023 Ilya (Marshal) <https://github.com/MarshalX>'
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
exclude_patterns = []

# myst

myst_heading_anchors = 4
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html?highlight=header-anchors#code-fences-using-colons
myst_enable_extensions = ['colon_fence']
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

html_theme_options = {
    'navigation_with_keys': True,
}
