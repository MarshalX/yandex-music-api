# Получение токена

## Через библиотеку (OAuth Device Flow)

Библиотека умеет получать OAuth-токен сама через OAuth Device Flow.
Метод **блокирующий** — он ждёт, пока вы подтвердите вход на странице Яндекса,
и возвращает объект `OAuthToken` с полями `access_token`, `refresh_token`,
`expires_in`, `token_type`.

```{important}
Хранение токена — ответственность вызывающего кода. Библиотека не сохраняет
токен на диск и не обновляет его по истечении `expires_in`. Сохраните
`access_token` (например, в файл или переменную окружения) и передавайте
его в конструктор `Client` / `ClientAsync` при следующих запусках.
```

::::{tab-set}

:::{tab-item} Синхронный

```python
from yandex_music import Client


def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')


client = Client()
token = client.device_auth(on_code=on_code)

# Сохраните токен, чтобы не проходить авторизацию заново.
print(f'access_token:  {token.access_token}')
print(f'refresh_token: {token.refresh_token}')
print(f'expires_in:    {token.expires_in}')

client.init()
print(client.me.account.login)
```

:::

:::{tab-item} Асинхронный

```python
import asyncio

from yandex_music import ClientAsync


async def main():
    def on_code(code):
        print(f'Откройте {code.verification_url} и введите код: {code.user_code}')

    client = ClientAsync()
    token = await client.device_auth(on_code=on_code)

    # Сохраните токен, чтобы не проходить авторизацию заново.
    print(f'access_token:  {token.access_token}')
    print(f'refresh_token: {token.refresh_token}')
    print(f'expires_in:    {token.expires_in}')

    await client.init()
    print(client.me.account.login)


asyncio.run(main())
```

:::

::::

## Через браузер (implicit OAuth)

Если Device Flow по каким-то причинам не подходит, токен можно получить прямо из браузера — без библиотеки и без сторонних инструментов.

1. _(Опционально)_ Откройте DevTools во вкладке **Network** и включите троттлинг — страница `music.yandex.ru` редиректит очень быстро, и без замедления сети вы не успеете скопировать адресную строку. Инструкции: [Chrome](https://www.browserstack.com/guide/how-to-perform-network-throttling-in-chrome), [Firefox](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/throttling/index.html).
2. Откройте ссылку <https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d>.
3. При необходимости авторизуйтесь и выдайте доступ приложению.
4. Браузер перенаправит вас на адрес вида:

   ```text
   https://music.yandex.ru/#access_token=AQAAAAYc***&token_type=bearer&expires_in=31535645
   ```

   Скопируйте URL до того, как сработает повторный редирект.
5. Токен — это значение параметра `access_token` в URL.

## Альтернативные способы

**Своё OAuth-приложение создать нельзя.** Если ни один из вариантов выше не подходит,
используйте официальные клиенты или сторонние инструменты:

- [Вебсайт](https://music-yandex-bot.ru/) (работает не для всех аккаунтов)
- Android-приложение: [APK-файл](https://github.com/MarshalX/yandex-music-token/releases)
- Расширение для [Google Chrome](https://chrome.google.com/webstore/detail/yandex-music-token/lcbjeookjibfhjjopieifgjnhlegmkib)
- Расширение для [Mozilla Firefox](https://addons.mozilla.org/en-US/firefox/addon/yandex-music-token/)

Каждый вариант выше позволяет скопировать токен. Код каждого варианта [открыт](https://github.com/MarshalX/yandex-music-token).

**Полезные ссылки:**

- [Скрипт получения токена из другого проекта для Яндекс Станции](https://github.com/AlexxIT/YandexStation/blob/master/custom_components/yandex_station/core/yandex_session.py)

Полученный токен можно передавать в конструктор классов `yandex_music.Client` и `yandex_music.ClientAsync`.
