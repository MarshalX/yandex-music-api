from setuptools import setup, find_packages


def requirements():
    """Создание листа зависимостей для этого проекта."""
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages(exclude=['tests*'])

with open('README.rst', 'r', encoding='utf-8') as f:
    setup(name='yandex-music',
          version='0.0.4',
          author='Il`ya Semyonov',
          author_email='Ilya@marshal.by',
          license='LGPLv3',
          url='https://github.com/MarshalX/yandex-music-api/',
          keywords='python yandex music api wrapper library питон яндекс музыка апи обёртка библиотека',
          description="Делаю то, что по каким-то причинам не сделала компания Yandex.",
          long_description=f.read(),
          packages=packages,
          install_requires=requirements(),
          include_package_data=True,
          classifiers=[
              'Development Status :: 2 - Pre-Alpha',
              'Natural Language :: Russian',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
              'Operating System :: OS Independent',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Multimedia :: Sound/Audio',
              'Topic :: Internet',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
              'Programming Language :: Python :: 3.8'
          ],)
