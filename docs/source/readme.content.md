# Введение

Эта библиотека предоставляет Python интерфейс для никем незадокументированного и сделанного только для себя API Яндекс Музыки.

Она совместима с версиями Python 3.7+ и поддерживает работу как с синхронным, так и с асинхронным (asyncio) кодом.

В дополнение к реализации чистого API данная библиотека имеет ряд классов-обёрток — объектов высокого уровня, дабы сделать разработку клиентов и скриптов простой и понятной. Вся документация была написана с нуля исходя из логического анализа в ходе обратной разработки (reverse engineering) API.

## Доступ к вашим данным Яндекс.Музыка

Начиная с версии [2.0.0](https://github.com/MarshalX/yandex-music-api/blob/a30082f4929e56381c870cb03103777ae29bcc6b/CHANGES.rst#%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-200) библиотека больше не предоставляет интерфейсы для работы с OAuth Яндекс и Яндекс.Паспорт. Задача по получению токена для доступа к данным лежит на плечах разработчиков, использующих данную библиотеку. О том как получить токен читайте в документации.

# Установка

Вы можете установить или обновить Yandex Music API с помощью команды:

``` shell
pip install -U yandex-music
```

Или Вы можете установить из исходного кода с помощью команды:

``` shell
git clone https://github.com/MarshalX/yandex-music-api
cd yandex-music-api
python setup.py install
```

# Начало работы

Приступив к работе, первым делом необходимо создать экземпляр клиента.

Инициализация синхронного клиента:

``` python
from yandex_music import Client

client = Client()
client.init()

# или

client = Client().init()
```

Инициализация асинхронного клиента:

``` python
from yandex_music import ClientAsync

client = ClientAsync()
await client.init()

# или

client = await Client().init()
```

Вызов `init()` необходим для получения информации — упрощения будущих запросов.

Работа без авторизации ограничена. Так, например, для загрузки будут доступны только первые 30 секунд аудиофайла. Для понимания всех ограничений зайдите на сайт Яндекс.Музыка в режиме инкогнито и воспользуйтесь сервисом.

Для доступа к личным данным следует авторизоваться. Это осуществляется через токен аккаунта Яндекс.Музыка.

Авторизация:

``` python
from yandex_music import Client

client = Client('token').init()
```

После успешного создания клиента Вы вольны в выборе необходимого метода из API. Все они доступны у объекта класса `Client`. Подробнее в методах клиента в [документации](https://yandex-music.readthedocs.io/en/latest/yandex_music.client.html).

Пример получения первого трека из плейлиста "Мне нравится" и его загрузки:

``` python
from yandex_music import Client

client = Client('token').init()
client.users_likes_tracks()[0].fetch_track().download('example.mp3')
```

В примере выше клиент получает список треков, которые были отмечены как понравившиеся. API возвращает объект [TracksList](https://yandex-music.readthedocs.io/en/latest/yandex_music.tracks_list.html), в котором содержится список с треками класса [TrackShort](https://yandex-music.readthedocs.io/en/latest/yandex_music.track_short.html). Данный класс содержит наиважнейшую информацию о треке и никаких подробностей, поэтому для получения полной версии трека со всей информацией необходимо обратиться к методу `fetch_track()`. Затем можно скачать трек методом `download()`.

Пример получения треков по ID:

``` python
from yandex_music import Client

client = Client().init()
client.tracks(['10994777:1193829', '40133452:5206873', '48966383:6693286', '51385674:7163467'])
```

В качестве ID трека выступает его уникальный номер и номер альбома. Первым треком из примера является следующий трек:music.yandex.ru/album/**1193829**/track/**10994777**

Выполнение запросов с использование прокси в синхронной версии:

``` python
from yandex_music.utils.request import Request
from yandex_music import Client

request = Request(proxy_url='socks5://user:password@host:port')
client = Client(request=request).init()
```

Примеры Proxy URL:
- socks5://user:<password@host>:port
- <http://host:port>
- <https://host:port>
- <http://user:password@host>

Больше примеров тут: [proxies - advanced usage - requests](https://2.python-requests.org/en/master/user/advanced/#proxies)

Выполнение запросов с использование прокси в асинхронной версии:

``` python
from yandex_music.utils.request_async import Request
from yandex_music import ClientAsync

request = Request(proxy_url='http://user:pass@some.proxy.com')
client = await ClientAsync(request=request).init()
```

Socks прокси не поддерживаются в асинхронной версии.

Про поддерживаемые прокси тут: [proxy support - advanced usage - aiohttp](https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support)

## Изучение по примерам

Вот несколько примеров для обзора. Даже если это не Ваш подход к обучению, пожалуйста, возьмите и бегло просмотрите их.

Код примеров опубликован в открытом доступе, поэтому Вы можете взять его и начать писать вокруг него свой.

Посетите [эту страницу](https://github.com/MarshalX/yandex-music-api/blob/main/examples/), чтобы изучить официальные примеры.

## Особенности использования асинхронного клиента

При работе с асинхронной версией библиотеке стоит всегда помнить
следующие особенности:
- Клиент следует импортировать с названием `ClientAsync`, а не просто `Client`.
- При использовании методов-сокращений нужно выбирать метод с суффиксом `_async`.

Пояснение ко второму пункту:

``` python
from yandex_music import ClientAsync

client = await ClientAsync('token').init()
liked_short_track = (await client.users_likes_tracks())[0]

# правильно
full_track = await liked_short_track.fetch_track_async()
await full_track.download_async()

# НЕПРАВИЛЬНО
full_track = await liked_short_track.fetch_track()
await full_track.download()
```

## Логирование

Данная библиотека использует модуль `logging`. Чтобы настроить логирование на стандартный вывод, поместите

``` python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

в начало вашего скрипта.

Вы также можете использовать логирование в вашем приложении, вызвав `logging.getLogger()` и установить уровень какой Вы хотите:

``` python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```

Если Вы хотите `DEBUG` логирование:

``` python
logger.setLevel(logging.DEBUG)
```

# Получение помощи

Получить помощь можно несколькими путями:
- Задать вопрос в [Telegram чате](https://t.me/yandex_music_api), где мы помогаем друг другу, присоединяйтесь\!
- Сообщить о баге можно [создав Bug Report](https://github.com/MarshalX/yandex-music-api/issues/new?assignees=MarshalX&labels=bug&template=bug-report.md&title=).
- Предложить новую фичу или задать вопрос можно [создав discussion](https://github.com/MarshalX/yandex-music-api/discussions/new).
- Найти ответ на вопрос в [документации библиотеки](https://yandex-music.readthedocs.io/en/latest/).

# Список изменений

Весь список изменений ведётся в файле [CHANGES.md](https://github.com/MarshalX/yandex-music-api/blob/main/CHANGES.md).

# Реализации на других языках

## C#

Реализация с совершенно другим подходом, так как используется API для frontend'a, а не мобильных и десктопных приложений: [Winster332/Yandex.Music.Api](https://github.com/Winster332/Yandex.Music.Api).

[@Winster332](https://github.com/Winster332) не сильно проявляет активность, но существует форк, который продолжил начатое. Эндпоинты изменены с фронтовых на мобильные: [K1llMan/Yandex.Music.Api](https://github.com/K1llMan/Yandex.Music.Api).

## PHP

Частично переписанная текущая библиотека на PHP: [LuckyWins/yandex-music-api](https://github.com/LuckyWins/yandex-music-api).

## JavaScript

API wrapper на NodeJS. Не обновлялся больше двух лет: [itsmepetrov/yandex-music-api](https://github.com/itsmepetrov/yandex-music-api). Продолжение разработки заброшенной библиотеки: [kontsevoye/ym-api](https://github.com/kontsevoye/ym-api).

# Разработанные проекты

## Плагин для Kodi

Плагин может проигрывать пользовательские плейлисты и плейлисты Яндекса, поиск по Яндекс Музыке, радио.

Сайт проекта: [ymkodi.ru](https://ymkodi.ru/). Исходный код: [kodi.plugin.yandex-music](https://github.com/Angel777d/kodi.plugin.yandex-music).
Автор: [@Angel777d](https://github.com/Angel777d).

[![Плагин для Kodi](https://raw.githubusercontent.com/Angel777d/kodi.plugin.yandex-music/master/assets/img/kody_yandex_music_plugin.png)](https://ymkodi.ru/)

## Telegram бот-клиент

Неофициальный бот. Умные и ваши плейлисты, понравившиеся треки. Лайки, дизлайки, текста песен, поиск, распознавание песен, похожие треки! Полноценный клиент на базе мессенджера.

Сайт проекта: [music-yandex-bot.ru](https://music-yandex-bot.ru/). Бот в Telegram: [@music\_yandex\_bot](https://t.me/music_yandex_bot). Автор: [@MarshalX](https://github.com/MarshalX).

Статья на habr.com с описанием реализации: [Под капотом бота-клиента Яндекс.Музыки](https://habr.com/ru/post/487428/).

[![Telegram бот-клиент](https://hsto.org/webt/uv/4s/a3/uv4sa3pslohuzlmuzrjzteju2dk.png)](https://music-yandex-bot.ru/)

# Благодарность

Спасибо разработчикам `python-telegram-bot`. Выбрал Вас в качестве примера.

# Спонсоры

## JetBrains

<img height="150" width="150" src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png" alt="JetBrains Logo (Main) logo.">

> JetBrains предоставляет бесплатный набор инструментов для разработки активным контрибьюторам некоммерческих проектов с открытым исходным кодом.

[Лицензии для проектов с открытым исходным кодом — Программы поддержки](https://jb.gg/OpenSourceSupport)
