import asyncio

from yandex_music import ClientAsync


def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')
    print(f'Код действителен {code.expires_in} секунд')


async def main():
    client = ClientAsync()
    token = await client.device_auth(on_code=on_code)

    # Сохраните токен, чтобы не проходить авторизацию при каждом запуске.
    # Библиотека не сохраняет токен на диск и не обновляет его автоматически.
    print(f'access_token:  {token.access_token}')
    print(f'refresh_token: {token.refresh_token}')
    print(f'expires_in:    {token.expires_in} сек')

    await client.init()
    print(f'Здравствуйте, {client.me.account.login}!')


if __name__ == '__main__':
    asyncio.run(main())
