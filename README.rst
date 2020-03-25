[Alpha] Неофициальная Python библиотека для API Yandex Music
============================================================

Делаю то, что по определённым причинам не сделала компания Yandex.

Маленькое сообщество разработчиков общаются и помогают друг другу
в `Telegram чатике <https://tx.me/yandex_music_api>`_, присоединяйтесь!

.. image:: https://img.shields.io/pypi/v/yandex-music.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Версия пакета PyPi

.. image:: https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8-blue.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Поддерживаемые Python версии

.. image:: https://codecov.io/gh/MarshalX/yandex-music-api/branch/development/graph/badge.svg
   :target: https://codecov.io/gh/MarshalX/yandex-music-api
   :alt: Покрытие кода тестами

.. image:: https://api.codacy.com/project/badge/Grade/27011a5a8d9f4b278d1bfe2fe8725fed
   :target: https://www.codacy.com/manual/MarshalX/yandex-music-api
   :alt: Качество кода

.. image:: https://github.com/MarshalX/yandex-music-api/workflows/Full%20test/badge.svg
   :target: https://github.com/MarshalX/yandex-music-api/actions?query=workflow%3A%22Full+test%22
   :alt: Статус тестов

.. image:: https://readthedocs.org/projects/yandex-music/badge/?version=latest
   :target: https://yandex-music.readthedocs.io/ru/latest/?badge=latest
   :alt: Статус документации

.. image:: https://img.shields.io/badge/license-LGPLv3-lightgrey.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: Лицензия LGPLv3

.. image:: https://img.shields.io/badge/telegram-чат-blue.svg
   :target: https://tx.me/yandex_music_api
   :alt: Telegram чат


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

- `Получение помощи`_

- `Реализации на других языках`_

  #. `C#`_

  #. `PHP`_

  #. `JavaScript`_

- `Разработанные проекты`_

  #. `Плагин для Kodi`_

  #. `Telegram бот-клиент`_

- `Благодарность`_

- `Лицензия`_

========
Введение
========

Эта библиотека предоставляется Python интерфейс для никем
незадокументированного и сделанного только для себя API Яндекс Музыки.

Она совместима с версиями Python 3.6+.

В дополнение к реализации чистого API данная библиотека имеет ряд
классов-обёрток объектов высокого уровня дабы сделать разработку клиентов
и скриптов простой и понятной.

--------------------------------
Доступ к вашим данным на Яндексе
--------------------------------

Значения констант
`CLIENT_ID и CLIENT_SECRET <https://github.com/MarshalX/yandex-music-api/blob/master/yandex_music/client.py#L11>`_
позаимствовано у официального приложения-клиента сервиса Яндекс.Музыка из магазина
Microsoft Store. Так как API является закрытым и используется только внутри
компании Яндекс сейчас невозможно зарегистрировать своё собственное приложение на
`oauth.yandex.ru <https://oauth.yandex.ru/>`_, а следовательно, использовать свои
значения констант.

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

Приступив к работе первым делом необходимо создать экземпляр клиента.

Инициализация клиента:

.. code:: python

    from yandex_music.client import Client

    client = Client()

Для доступа к своим личным данным следует авторизоваться.
Это можно осуществить через OAuth токен или логин с паролем.

Авторизация по логину и паролю:

.. code:: python

    from yandex_music.client import Client

    client = Client.from_credentials('example@yandex.com', 'password')

Авторизация по токену:

.. code:: python

    from yandex_music.client import Client

    client = Client.from_token('token')
    # или
    client = Client('token')

После успешного создания клиента Вы вольны в выборе необходимого метода
из API. Все они доступны у объекта класса Client. Подробнее в методах клиента
в `документации <https://yandex-music.readthedocs.io/ru/latest/yandex_music.client.html>`_.

Пример получения первого трека из плейлиста "Мне нравится" и его загрузка:

.. code:: python

    from yandex_music.client import Client

    client = Client.from_credentials('example@yandex.com', 'password')
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

    client = Client()
    client.tracks(['10994777:1193829', '40133452:5206873', '48966383:6693286', '51385674:7163467'])

В качестве ID трека выступает его уникальный номер и номер альбома.
Первым треком из примера является следующий трек:
music.yandex.ru/album/**1193829**/track/**10994777**

Выполнение запросов с использование прокси:

.. code:: python

    from yandex_music.utils.request import Request
    from yandex_music.client import Client

    request = Request(proxy_url='socks5://user:password@host:port')
    client = Client(request=request)

Примеры proxy url:

- socks5://user:password@host:port
- http://host:port
- https://host:port
- http://user:password@host

Больше примеров тут: `proxies - advanced usage - requests <https://2.python-requests.org/en/master/user/advanced/#proxies>`_

Пример инициализации клиента с обработкой капчи:

.. code:: python

    def init_client():
        client = captcha_key = captcha_answer = None
        while not client:
            try:
                client = Client.from_credentials('login', 'pass', captcha_answer, captcha_key)
            except Captcha as e:
                e.captcha.download('captcha.png')

                captcha_key = e.captcha.x_captcha_key
                captcha_answer = input('Число с картинки: ')

        return client

Пример инициализации клиента с обработкой капчи при помощи callback-функции:

.. code:: python

    def proc_captcha(captcha):
        captcha.download('captcha.png')
        return input('Число с картинки: ')

    client = Client.from_credentials('login', 'pass', captcha_callback=proc_captcha)

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

Данная библиотека использует ``logging`` модуль. Чтобы настроить логирование на
стандартный вывод, поместите

.. code:: python

    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

в начало вашего скрипта.

Вы также можете использовать логирование в вашем приложении, вызвав
``logging.getLogger()`` и установить уровень какой Вы хотите:

.. code:: python

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

Если Вы хотите DEBUG логирование:

.. code:: python

    logger.setLevel(logging.DEBUG)

============
Документация
============

Документация ``yandex-music-api`` расположена на
`readthedocs.io <https://yandex-music.readthedocs.io/>`_.
Вашей отправной точкой должен быть класс ``Client``, а точнее его методы. Именно они выполняют все
запросы на API и возвращают Вам готовые объекты.
`Класс Client на readthedocs.io <https://yandex-music.readthedocs.io/ru/latest/yandex_music.client.html>`_.

================
Получение помощи
================

Получить помощь можно несколькими путями:

- Задать вопрос в `Telegram чатике <https://tx.me/yandex_music_api>`_, где мы помогаем друг другу, присоединяйтесь!
- Сообщить о баге, предложить новую фичу или задать вопрос можно `создав issue <https://github.com/MarshalX/yandex-music-api/issues/new/choose>`_.
- Найти ответ на вопрос в `документации библиотеки <https://yandex-music.readthedocs.io/ru/latest/>`_.

===========================
Реализации на других языках
===========================

--
C#
--

Реализация с совершенно другим подходом, так как используется API для frontend'a,
а не мобильных и десктопных приложений:
`Winster332/Yandex.Music.Api <https://github.com/Winster332/Yandex.Music.Api>`_.

Автор не сильно проявляет активность, но появился форк, который продолжил начатое. Более того,
`@K1llMan <https://github.com/K1llMan>`_ (автор форка) планирует изменить эндпоинты с фронтовых на
те, что используются в данной библиотеке.
`K1llMan/Yandex.Music.Api <https://github.com/K1llMan/Yandex.Music.Api>`_

---
PHP
---

Частично переписанная текущая библиотека на PHP:
`LuckyWins/yandex-music-api <https://github.com/LuckyWins/yandex-music-api>`_.

----------
JavaScript
----------

API wrapper на Node.JS. Не обновлялся больше двух лет:
`itsmepetrov/yandex-music-api <https://github.com/itsmepetrov/yandex-music-api>`_.

=====================
Разработанные проекты
=====================

---------------
Плагин для Kodi
---------------

Плагин может проигрывать пользовательские плейлисты и плейлисты Яндекса, поиск по Яндекс Музыке, радио.

Сайт проекта: `ymkodi.ml <https://ymkodi.ml/>`_.

Исходный код: `kodi.plugin.yandex-music  <https://github.com/Angel777d/kodi.plugin.yandex-music>`_

Автор: `@Angel777d <https://github.com/Angel777d>`_

.. image:: https://raw.githubusercontent.com/Angel777d/kodi.plugin.yandex-music/master/assets/img/kody_yandex_music_plugin.png
   :target: https://ymkodi.ml/
   :alt: Плагин для Kodi

-------------------
Telegram бот-клиент
-------------------

Неофициальный бот. Умные и ваши плейлисты, понравившиеся треки. Лайки, дизлайки, текста песен,
поиск, распознавание песен, похожие треки! Полноценный клиент на базе мессенджера.

Сайт проекта: `music-yandex-bot.ru <https://music-yandex-bot.ru/>`_

Username в Telegram: `@music_yandex_bot <https://tx.me/music_yandex_bot>`_

Статья на habr.com с описанием реализации: `Под капотом бота-клиента Яндекс.Музыки <https://habr.com/ru/post/487428/>`_

Автор: `@MarshalX <https://marshal.by/>`_

.. image:: https://hsto.org/webt/uv/4s/a3/uv4sa3pslohuzlmuzrjzteju2dk.png
   :target: https://music-yandex-bot.ru/
   :alt: Telegram бот-клиент

=============
Благодарность
=============

Спасибо разработчикам ``python-telegram-bot``. Выбрал Вас в качестве примера.

========
Лицензия
========

Вы можете копировать, распространять и модифицировать программное обеспечение
при условии, что модификации описаны и лицензированы бесплатно в соответствии
с  `LGPL-3 <https://www.gnu.org/licenses/lgpl-3.0.html>`_. Произведения
производных (включая модификации или что-либо статически связанное с библиотекой)
могут распространяться только в соответствии с  LGPL-3, но приложения, которые
используют библиотеку, необязательно.
