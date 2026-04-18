# Получение токена через Device Flow

Пример получения OAuth-токена через OAuth Device Flow без сторонних инструментов.
Метод `device_auth` блокирующий: он ждёт, пока вы подтвердите вход на странице
Яндекса, и возвращает `OAuthToken` с полями `access_token`, `refresh_token`,
`expires_in`, `token_type`. Сохранять токен (например, в файл или БД) —
ответственность вызывающего кода.

::::{tab-set}

:::{tab-item} Синхронный

```python
from yandex_music import Client


def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')
    print(f'Код действителен {code.expires_in} секунд')


client = Client()
token = client.device_auth(on_code=on_code)

print(f'access_token:  {token.access_token}')
print(f'refresh_token: {token.refresh_token}')
print(f'expires_in:    {token.expires_in} сек')

client.init()
print(f'Здравствуйте, {client.me.account.login}!')
```

:::

:::{tab-item} Асинхронный

```python
import asyncio

from yandex_music import ClientAsync


def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')
    print(f'Код действителен {code.expires_in} секунд')


async def main():
    client = ClientAsync()
    token = await client.device_auth(on_code=on_code)

    print(f'access_token:  {token.access_token}')
    print(f'refresh_token: {token.refresh_token}')
    print(f'expires_in:    {token.expires_in} сек')

    await client.init()
    print(f'Здравствуйте, {client.me.account.login}!')


if __name__ == '__main__':
    asyncio.run(main())
```

:::

::::
