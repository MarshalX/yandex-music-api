import re
import sys
import json

from setuptools import setup, find_packages
from setuptools.command.test import test


class PyTest(test):
    def run_tests(self):
        import pytest
        sys.exit(pytest.main(['tests']))


def requirements(section):
    """Создание листа зависимостей для этого проекта."""
    with open('Pipfile.lock') as pip_file:
        pipfile_json = json.load(pip_file)

    return [package + detail.get('version', '')
            for package, detail in pipfile_json[section].items()]


packages = find_packages()

with open('yandex_music/__init__.py', encoding='utf-8') as f:
    version = re.findall(r"__version__ = '(.+)'", f.read())[0]

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('CHANGES.rst', 'r', encoding='utf-8') as f:
    changes = f.read()


setup(name='yandex-music',
      version=version,
      author='Il`ya Semyonov',
      author_email='ilya@marshal.dev',
      license='LGPLv3',
      url='https://github.com/MarshalX/yandex-music-api/',
      keywords='python yandex music api wrapper library client питон пайтон '
               'яндекс музыка апи обёртка библиотека клиент',
      description='Делаю то, что по определённым причинам не сделала компания Yandex.',
      long_description=f'{readme}\n{changes}',
      packages=packages,
      install_requires=requirements('default'),
      include_package_data=True,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Natural Language :: Russian',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Operating System :: OS Independent',
          'Topic :: Internet',
          'Topic :: Multimedia :: Sound/Audio',
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Libraries :: Application Frameworks",
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          "Programming Language :: Python :: Implementation",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"
      ],
      python_requires="~=3.6",
      cmdclass={'test': PyTest},
      tests_require=requirements('develop'),
      project_urls={
          'Code': 'https://github.com/MarshalX/yandex-music-api',
          'Documentation': 'https://yandex-music.readthedocs.io',
          'Chat': 'https://t.me/yandex_music_api',
          'Codecov': 'https://codecov.io/gh/MarshalX/yandex-music-api',
          'Codacy': 'https://www.codacy.com/manual/MarshalX/yandex-music-api',
      })
