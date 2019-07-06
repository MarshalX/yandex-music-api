Неофициальная Python библиотека для API Yandex Music
====================================================

Делаю то, что по каким-то причинам не сделала компания Yandex.

.. image:: https://img.shields.io/pypi/v/yandex-music.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Версия пакета PyPi

.. image:: https://img.shields.io/badge/python-3.6%2B-blue.svg
   :target: https://pypi.org/project/yandex-music/
   :alt: Поддерживаемые Python версии

.. image:: https://img.shields.io/badge/docs-%D0%B2%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B5-red.svg
   :target: https://yandex-music.readthedocs.io/
   :alt: Статус документации

.. image:: https://img.shields.io/badge/license-LGPLv3-lightgrey.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: Лицензия LGPLv3


==========
Содержание
==========

- `Введение`_

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

Она совместима с версиями Python 3.6+.

В дополнение к реализации чистого API данная библиотека имеет ряд
классов-обёрток объектов высокого уровня дабы сделать разработку клиентов
и скриптов простой и понятной.

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

Полезные ссылки:

- `Документация yandex-music-api <https://yandex-music.readthedocs.io/>`_

--------------------
Изучение по примерам
--------------------

Вот несколько примеров для обзора. Даже если это не Ваш подход к
обучению, пожалуйста, возьмите и бегло просмотрите их.

Код примеров опубликован в открытом доступе, поэтому
Вы можете взять его и начать писать вокруг своё.

Посетите `эту страницу <https://github.com/MarshalX/yandex-music-api/blob/master/examples/README.md>`_
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