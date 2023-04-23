# Получение токена

**Своё OAuth приложение создать нельзя.** Единственный вариант это использовать приложения официальных клиентов Яндекс.Музыка. 

**Существует основные варианты получения токена:**
- [Вебсайт](https://music-yandex-bot.ru/) (работает не для всех аккаунтов)
- Android приложение: [APK файл](https://github.com/MarshalX/yandex-music-token/releases)
- Расширение для [Google Chrome](https://chrome.google.com/webstore/detail/yandex-music-token/lcbjeookjibfhjjopieifgjnhlegmkib)
- Расширение для [Mozilla Firefox](https://addons.mozilla.org/en-US/firefox/addon/yandex-music-token/)

Каждый вариант выше позволяет скопировать токен. Код каждого варианта [открыт](https://github.com/MarshalX/yandex-music-token).

**Полезные ссылки:**
- [Способ вместо расширения для продвинутых](https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781)
- [Скрипт получения токена из другого проекта для Яндекс Станции](https://github.com/AlexxIT/YandexStation/blob/master/custom_components/yandex_station/core/yandex_session.py)

Полученный токен можно передавать в конструктор классов `yandex_music.Client` и `yandex_client.ClientAsync`.
