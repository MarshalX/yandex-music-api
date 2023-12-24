"""Setup script for yandex-music-api."""
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test


class PyTest(test):
    """PyTest test runner."""

    def run_tests(self) -> None:
        """Run tests."""
        import pytest

        sys.exit(pytest.main(['tests']))


with open('yandex_music/__init__.py', encoding='UTF-8') as f:
    version = re.findall(r"__version__ = '(.+)'", f.read())[0]

with open('README.md', 'r', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='yandex-music',
    version=version,
    author='Ilya (Marshal)',
    author_email='ilya@marshal.dev',
    license='LGPLv3',
    url='https://github.com/MarshalX/yandex-music-api/',
    keywords='python yandex music api wrapper library client питон пайтон '
    'яндекс музыка апи обёртка библиотека клиент',
    description='Неофициальная Python библиотека для работы с API сервиса Яндекс.Музыка.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests[socks]', 'aiohttp', 'aiofiles'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='~=3.7',
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    project_urls={
        'Documentation': 'https://yandex-music.rtfd.io',
        'Changes': 'https://github.com/MarshalX/yandex-music-api/blob/main/CHANGES.md',
        'Tracker': 'https://github.com/MarshalX/yandex-music-api/issues',
        'Telegram chat': 'https://t.me/yandex_music_api',
        'Codecov': 'https://codecov.io/gh/MarshalX/yandex-music-api',
        'Codacy': 'https://app.codacy.com/gh/MarshalX/yandex-music-api',
    },
)
