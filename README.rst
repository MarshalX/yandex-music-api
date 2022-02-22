================
Yandex Music API
================

    Делаю то, что по определённым причинам не сделала компания Yandex.

⚠️ Это неофициальная библиотека.

Сообщество разработчиков общаются и помогают друг другу
в `Telegram чате <https://t.me/yandex_music_api>`_, присоединяйтесь!

.. image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Поддерживаемые Python версии

.. image:: https://codecov.io/gh/MarshalX/yandex-music-api/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/MarshalX/yandex-music-api
   :alt: Покрытие кода тестами

.. image:: https://api.codacy.com/project/badge/Grade/27011a5a8d9f4b278d1bfe2fe8725fed
   :target: https://www.codacy.com/manual/MarshalX/yandex-music-api
   :alt: Качество кода

.. image:: https://github.com/MarshalX/yandex-music-api/actions/workflows/pytest_full.yml/badge.svg
   :target: https://github.com/MarshalX/yandex-music-api/actions/workflows/pytest_full.yml
   :alt: Статус тестов

.. image:: https://readthedocs.org/projects/yandex-music/badge/?version=latest
   :target: https://yandex-music.readthedocs.io/en/latest/?badge=latest
   :alt: Статус документации

.. image:: https://img.shields.io/badge/license-LGPLv3-lightgrey.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: Лицензия LGPLv3


==========
Содержание
==========

- `Введение`_

  #. `Доступ к вашим данным Яндекс.Музыка`_

- `Установка`_

- `Начало работы`_

  #. `Изучение по примерам`_

  #. `Особенности использования асинхронного клиента`_

  #. `Логирование`_

  #. `Документация`_

- `Получение помощи`_

- `Список изменений`_

- `Реализации на других языках`_

  #. `C#`_

  #. `PHP`_

  #. `JavaScript`_

- `Разработанные проекты`_

  #. `Плагин для Kodi`_

  #. `Telegram бот-клиент`_

- `Благодарность`_

- `Внесение своего вклада в проект`_

- `Лицензия`_

========
Введение
========

Эта библиотека предоставляется Python интерфейс для никем
незадокументированного и сделанного только для себя API Яндекс Музыки.

Она совместима с версиями Python 3.7+ и поддерживает работу как с синхронном,
так и асинхронным (asyncio) кодом.

В дополнение к реализации чистого API данная библиотека имеет ряд
классов-обёрток объектов высокого уровня дабы сделать разработку клиентов
и скриптов простой и понятной. Вся документация была написана с нуля исходя
из логического анализа в ходе обратной разработки (reverse engineering) API.

-----------------------------------
Доступ к вашим данным Яндекс.Музыка
-----------------------------------

Начиная с версии `2.0.0 <https://github.com/MarshalX/yandex-music-api/blob/main/CHANGES.rst#%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-200>`_ библиотека больше не предоставляет интерфейсы для работы
с OAuth Яндекс и Яндекс.Паспорт. Задача по получению токена для доступа к данным
на плечах разработчиков использующих данную библиотеку.

=========
Установка
=========

Вы можете установить или обновить Yandex Music API при помощи:

.. code:: shell

    pip install yandex-music --upgrade

Или Вы можете установить из исходного кода с помощью:

.. code:: shell

    git clone https://github.com/MarshalX/yandex-music-api
    cd yandex-music-api
    python setup.py install

=============
Начало работы
=============

Приступив к работе первым делом необходимо создать экземпляр клиента.

Инициализация синхронного клиента:

.. code:: python

    from yandex_music import Client

    client = Client()
    client.init()

    # или

    client = Client().init()

Инициализация асинхронного клиента:

.. code:: python

    from yandex_music import ClientAsync

    client = ClientAsync()
    await client.init()

    # или

    client = await Client().init()

Вызов ``init()`` необходим для получение информации для упрощения будущих запросов.

Работа без авторизации ограничена. Так, например, для загрузки будут доступны
только первые 30 секунд аудиофайла. Для понимания всех ограничений зайдите на
сайт Яндекс.Музыка под инкогнито и воспользуйтесь сервисом.

Для доступа к своим личным данным следует авторизоваться.
Это осуществляется через токен аккаунта Яндекс.Музыка.

Авторизация:

.. code:: python

    from yandex_music import Client

    client = Client('token').init()

После успешного создания клиента Вы вольны в выборе необходимого метода
из API. Все они доступны у объекта класса ``Client``. Подробнее в методах клиента
в `документации <https://yandex-music.readthedocs.io/en/latest/yandex_music.client.html>`_.

Пример получения первого трека из плейлиста "Мне нравится" и его загрузка:

.. code:: python

    from yandex_music import Client

    client = Client('token').init()
    client.users_likes_tracks()[0].fetch_track().download('example.mp3')

В примере выше клиент получает список треков которые были отмечены как
понравившиеся. API возвращает объект
`TracksList <https://yandex-music.readthedocs.io/en/latest/yandex_music.tracks_list.html>`_
в котором содержится список с треками класса
`TrackShort <https://yandex-music.readthedocs.io/en/latest/yandex_music.track_short.html>`_.
Данный класс содержит наиважнейшую информацию о треке и никаких подробностей,
поэтому для получения полной версии трека со всей информацией необходимо
обратиться к методу ``fetch_track()``. Затем можно скачать трек методом ``download()``.

Пример получения треков по ID:

.. code:: python

    from yandex_music import Client

    client = Client().init()
    client.tracks(['10994777:1193829', '40133452:5206873', '48966383:6693286', '51385674:7163467'])

В качестве ID трека выступает его уникальный номер и номер альбома.
Первым треком из примера является следующий трек:
music.yandex.ru/album/**1193829**/track/**10994777**

Выполнение запросов с использование прокси в синхронной версии:

.. code:: python

    from yandex_music.utils.request import Request
    from yandex_music import Client

    request = Request(proxy_url='socks5://user:password@host:port')
    client = Client(request=request).init()

Примеры proxy url:

- socks5://user:password@host:port
- http://host:port
- https://host:port
- http://user:password@host

Больше примеров тут: `proxies - advanced usage - requests <https://2.python-requests.org/en/master/user/advanced/#proxies>`_

Выполнение запросов с использование прокси в асинхронной версии:

.. code:: python

    from yandex_music.utils.request_async import Request
    from yandex_music import ClientAsync

    request = Request(proxy_url='http://user:pass@some.proxy.com')
    client = await ClientAsync(request=request).init()

Socks прокси не поддерживаются в асинхронной версии.

Про поддерживаемые прокси тут: `proxy support - advanced usage - aiohttp <https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support>`_

--------------------
Изучение по примерам
--------------------

Вот несколько примеров для обзора. Даже если это не Ваш подход к
обучению, пожалуйста, возьмите и бегло просмотрите их.

Код примеров опубликован в открытом доступе, поэтому
Вы можете взять его и начать писать вокруг своё.

Посетите `эту страницу <https://github.com/MarshalX/yandex-music-api/blob/main/examples/>`_
чтобы изучить официальные примеры.

----------------------------------------------
Особенности использования асинхронного клиента
----------------------------------------------

При работе с асинхронной версией библиотеке стоит всегда помнить
следующие особенности:

- Клиент следует импортировать с названием ``ClientAsync``, а не просто ``Client``.
- При использовании методов-сокращений нужно выбирать метод с суффиксом ``_async``.

Пояснение ко второму пункту:

.. code:: python

    from yandex_music import ClientAsync

    client = await ClientAsync('token').init()
    liked_short_track = (await client.users_likes_tracks())[0]

    # правильно
    full_track = await liked_short_track.fetch_track_async()
    await full_track.download_async()

    # НЕПРАВИЛЬНО
    full_track = await liked_short_track.fetch_track()
    await full_track.download()

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

Если Вы хотите ``DEBUG`` логирование:

.. code:: python

    logger.setLevel(logging.DEBUG)

============
Документация
============

Документация ``yandex-music-api`` расположена на
`readthedocs.io <https://yandex-music.readthedocs.io/>`_.
Вашей отправной точкой должен быть класс ``Client``, а точнее его методы.
Именно они выполняют все
запросы на API и возвращают Вам готовые объекты.
`Класс Client на readthedocs.io <https://yandex-music.readthedocs.io/en/latest/yandex_music.client.html>`_.

================
Получение помощи
================

Получить помощь можно несколькими путями:

- Задать вопрос в `Telegram чате <https://t.me/yandex_music_api>`_, где мы помогаем друг другу, присоединяйтесь!
- Сообщить о баге можно `создав Bug Report <https://github.com/MarshalX/yandex-music-api/issues/new?assignees=MarshalX&labels=bug&template=bug-report.md&title=>`_.
- Предложить новую фичу или задать вопрос можно `создав discussion <https://github.com/MarshalX/yandex-music-api/discussions/new>`_.
- Найти ответ на вопрос в `документации библиотеки <https://yandex-music.readthedocs.io/en/latest/>`_.

================
Список изменений
================

Весь список изменений ведётся в файле `CHANGES.rst <https://github.com/MarshalX/yandex-music-api/blob/main/CHANGES.rst>`_.


===========================
Реализации на других языках
===========================

--
C#
--

Реализация с совершенно другим подходом, так как используется API для frontend'a,
а не мобильных и десктопных приложений:
`Winster332/Yandex.Music.Api <https://github.com/Winster332/Yandex.Music.Api>`_.

`@Winster332 <https://github.com/Winster332>`_ не сильно проявляет активность,
но существует форк, который продолжил начатое. Эндпоинты изменены с фронтовых на
мобильные: `K1llMan/Yandex.Music.Api <https://github.com/K1llMan/Yandex.Music.Api>`_.

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
Продолжение разработки заброшенной библиотеки: `kontsevoye/ym-api <https://github.com/kontsevoye/ym-api>`_.

=====================
Разработанные проекты
=====================

---------------
Плагин для Kodi
---------------

Плагин может проигрывать пользовательские плейлисты и плейлисты Яндекса, поиск
по Яндекс Музыке, радио.

Сайт проекта: `ymkodi.ru <https://ymkodi.ru/>`_.
Исходный код: `kodi.plugin.yandex-music  <https://github.com/Angel777d/kodi.plugin.yandex-music>`_.
Автор: `@Angel777d <https://github.com/Angel777d>`_.

.. image:: https://raw.githubusercontent.com/Angel777d/kodi.plugin.yandex-music/master/assets/img/kody_yandex_music_plugin.png
   :target: https://ymkodi.ru/
   :alt: Плагин для Kodi

-------------------
Telegram бот-клиент
-------------------

Неофициальный бот. Умные и ваши плейлисты, понравившиеся треки. Лайки, дизлайки, текста песен,
поиск, распознавание песен, похожие треки! Полноценный клиент на базе мессенджера.

Сайт проекта: `music-yandex-bot.ru <https://music-yandex-bot.ru/>`_.
Бот в Telegram: `@music_yandex_bot <https://t.me/music_yandex_bot>`_.
Автор: `@MarshalX <https://github.com/MarshalX>`_.

Статья на habr.com с описанием реализации: `Под капотом бота-клиента Яндекс.Музыки <https://habr.com/ru/post/487428/>`_.

.. image:: https://hsto.org/webt/uv/4s/a3/uv4sa3pslohuzlmuzrjzteju2dk.png
   :target: https://music-yandex-bot.ru/
   :alt: Telegram бот-клиент

=============
Благодарность
=============

Спасибо разработчикам ``python-telegram-bot``. Выбрал Вас в качестве примера.

===============================
Внесение своего вклада в проект
===============================

Внесение своего вклада максимально приветствуется! Есть перечень пунктов,
который стоит соблюдать. Каждый пункт перечня расписан в `CONTRIBUTING.md <https://github.com/MarshalX/yandex-music-api/blob/main/CONTRIBUTING.md>`_.

Вы можете помочь и сообщив о `баге <https://github.com/MarshalX/yandex-music-api/issues/new?assignees=MarshalX&labels=bug&template=bug-report.md&title=>`_
или о `новом поле пришедшем от API <https://github.com/MarshalX/yandex-music-api/issues/new?assignees=&labels=feature&template=found-unknown-fields.md&title=%D0%9D%D0%BE%D0%B2%D0%BE%D0%B5+%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D0%BE%D0%B5+%D0%BF%D0%BE%D0%BB%D0%B5+%D0%BE%D1%82+API>`_.

========
Лицензия
========

Вы можете копировать, распространять и модифицировать программное обеспечение
при условии, что модификации описаны и лицензированы бесплатно в соответствии
с  `LGPL-3 <https://www.gnu.org/licenses/lgpl-3.0.html>`_. Произведения
производных (включая модификации или что-либо статически связанное с библиотекой)
могут распространяться только в соответствии с  LGPL-3, но приложения, которые
используют библиотеку, необязательно.
