import os

from yandex_music import Client
from yandex_music.exceptions import YandexMusicError
from yandex_music.utils.request import Request

yandex_music_token = os.environ.get('YANDEX_MUSIC_TOKEN')
proxied_request = Request(proxy_url=os.environ.get('PROXY_URL'))

try:
    if not yandex_music_token:
        raise YandexMusicError

    # подключаемся без прокси для получения информации об аккаунте (доступно из других стран)
    client = Client(yandex_music_token, request=Request()).init()
    # проверяем отсутствие подписки у пользователя
    if client.me and client.me.plus and not client.me.plus.has_plus:
        # если подписки нет - пересоздаем клиент с использованием прокси
        client = Client(yandex_music_token, request=proxied_request).init()
except YandexMusicError:
    # если есть проблемы с авторизацией, токеном или чем-либо еще, то инициализируем клиент без авторизации
    # так как сервисом можно пользоваться будучи гостем, но со своими ограничениями
    client = Client(request=proxied_request)
