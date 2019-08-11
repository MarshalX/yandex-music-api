[Pre-Alpha] Неофициальная Python библиотека для API Yandex Music
================================================================

Делаю то, что по каким-то причинам не сделала компания Yandex.

.. image:: https://img.shields.io/pypi/v/yandex-music.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Версия пакета PyPi

.. image:: https://img.shields.io/badge/python-3.7%2B-blue.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Поддерживаемые Python версии

.. image:: https://readthedocs.org/projects/yandex-music/badge/?version=latest
    :target: https://yandex-music.readthedocs.io/ru/latest/?badge=latest
    :alt: Статус документации

.. image:: https://img.shields.io/badge/license-LGPLv3-lightgrey.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: Лицензия LGPLv3


==========
Содержание
==========

- `Введение`_

  #. `Доступ к вашим данным на Яндексе`_

- `Установка`_

- `Начало работы`_

  #. `Изучение по примерам`_

  #. `Логирование`_

  #. `Документация`_

- `Благодарность`_

- `Лицензия`_

========
Введение
========

Эта библиотека предоставляется Python интерфейс для никем
незадокументированного и сделанного только для себя API Яндекс Музыки.

Она совместима с версиями Python 3.7+.

В дополнение к реализации чистого API данная библиотека имеет ряд
классов-обёрток объектов высокого уровня дабы сделать разработку клиентов
и скриптов простой и понятной.

--------------------------------
Доступ к вашим данным на Яндексе
--------------------------------

Значения констант `CLIENT_ID и CLIENT_SECRET <https://github.com/MarshalX/yandex-music-api/blob/master/yandex_music/client.py#L11>`_
позаимствовано у официального приложения-клиента сервиса Яндекс.Музыка из магазина Microsoft Store. Так как API является
закрытым и используется только внутри компании Яндекс сейчас невозможно зарегистрировать своё собственное приложение на
`oauth.yandex.ru <https://oauth.yandex.ru/>`_, а следовательно, использовать свои значения констант.

=========
Установка
=========

**Библиотека находится в стадии разработки**

Вы можете установить или обновить yandex-music-api при помощи:

.. code:: shell

    $ pip install yandex-music --upgrade

Или Вы можете установить из исходного кода с помощью:

.. code:: shell

    $ git clone https://github.com/MarshalX/yandex-music-api --recursive
    $ cd yandex-music-api
    $ python setup.py install

=============
Начало работы
=============

Приступив к работе первом делом необходимо создать экземпляр клиента
введя данные для авторизации. Такими данными может служить OAuth токен или
логин с паролем.

Авторизация по логину и паролю:

.. code:: python

    from yandex_music.client import Client

    client = Client('example@yandex.com', 'password')

Авторизация по токену:

.. code:: python

    from yandex_music.client import Client

    client = Client.from_token('token')

После успешного создания клиента Вы вольны в выборе необходимого метода
из API. Все они доступны у объекта класса Client. Подробнее в методах клиента
в `документации <https://yandex-music.readthedocs.io/ru/latest/yandex_music.client.html>`_.

Пример получения первого трека из плейлиста "Мне нравится" и его загрузка:

.. code:: python

    from yandex_music.client import Client

    client = Client('example@yandex.com', 'password')
    client.users_likes_tracks()[0].track.download('example.mp3')

В примере выше клиент получает список треков которые были отмечены как
понравившиеся. API возвращает объект
`TracksList <https://yandex-music.readthedocs.io/ru/latest/yandex_music.tracks_list.html>`_
в котором содержится список с треками класса
`TrackShort <https://yandex-music.readthedocs.io/ru/latest/yandex_music.track_short.html>`_.
Данные класс содержит наиважнейшую информацию о треке и никаких подробностей,
поэтому для получения полной версии трека со всей информацией необходимо
обратиться к свойству track. Затем можно скачать трек методом download().

Пример получения треков по ID:

.. code:: python

    from yandex_music.client import Client

    client = Client('example@yandex.com', 'password')
    client.tracks(['10994777:1193829', '40133452:5206873', '48966383:6693286', '51385674:7163467'])

--------------------
Изучение по примерам
--------------------

Вот несколько примеров для обзора. Даже если это не Ваш подход к
обучению, пожалуйста, возьмите и бегло просмотрите их.

Код примеров опубликован в открытом доступе, поэтому
Вы можете взять его и начать писать вокруг своё.

Посетите `эту страницу <https://github.com/MarshalX/yandex-music-api/blob/master/examples/>`_
чтобы изучить официальные примеры.

-----------
Логирование
-----------

Данная библиотека использует ``logging`` модуль. Чтобы настроить логирование на стандартный вывод, поместите

.. code:: python

    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

в начало вашего скрипта.

Вы также можете использовать логирование в вашем приложении, вызвав ``logging.getLogger()`` и установить уровень какой Вы хотите:

.. code:: python

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

Если Вы хотите DEBUG логирование:

.. code:: python

    logger.setLevel(logging.DEBUG)

=============
Документация
=============

Документация ``yandex-music-api`` находится в стадии написания и расположена на `readthedocs.io <https://yandex-music.readthedocs.io/>`_.

=============
Благодарность
=============

Спасибо разработчикам ``python-telegram-bot``. Выбрал Вас в качестве примера.

========
Лицензия
========

Вы можете копировать, распространять и модифицировать программное обеспечение при условии, что модификации описаны и лицензированы бесплатно в соответствии с  `LGPL-3 <https://www.gnu.org/licenses/lgpl-3.0.html>`_. Произведения производных (включая модификации или что-либо статически связанное с библиотекой) могут распространяться только в соответствии с  LGPL-3, но приложения, которые используют библиотеку, необязательно.
