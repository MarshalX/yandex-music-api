# Примеры

Для того чтобы не вводить данные каждый раз при входе - достаточно сохранить токен.
```python
# Сначала подключаются необходимые модули
# Для собственно аутентификация на Яндекс Музыке
from yandex_music.client import Client
# Для проверки пароля
from yandex_music.exceptions import BadRequest
# Для скрытия ввода пароля с консоли
from getpass import getpass
# Для удобного сохранения токена
import json

# Задается имя файла
filename = 'credentials.json'
# Ввод пользователем учетных данных
login = input("Логин, почта или телефон: ")
password = getpass("Пароль: ")

try:
    # Попытка аутентификации
    client = Client.from_credentials(login, password)
except BadRequest:
    print("Неверный пароль")
else:
    # Если вход выполнен - сохраняется токен
    with open(filename, "w") as file:
        json.dump({"token": client.token},file)
    print(f"Токен успешно сохранен в '{filename}'")
```
С помощью этой библиотеки можно к примеру вывести список с десяти последних лайкнутых композиций.
```python
# Вход с помощью сохраненного ранее токена
with open("credentials.json") as file:
    credentials = json.load(file)
token = credentials["token"]
client = Client(token)

# Вывод данных композиции в нужном формате
def print_artist_title(track_short):
    # Для получения нужных значений обращаемся к свойству track объекта класа TrackShort
    track = track_short.track
    # вывод должен быть в формате {Исполнитель} - {Название трека}
    # например: Apocalyptica - I Don't Care
    print(track.artists[0]["name"],'-',track.title)

# Запрос на получения списка лайкнутых композиций
liked_tracks = client.users_likes_tracks()
# Вывод 10 последних
for track in liked_tracks[:10]:
    print_artist_title(track)
```

В этой папке есть небольшие примеры, чтобы показать как выглядят скрипты,
написанные с помощью `yandex-music-api`.

Все примеры лицензированы в соответствии с 
[Лицензией CC0] (https://github.com/MarshalX/yandex-music-api/blob/master/examples/LICENSE.txt) 
и поэтому полностью предназначены для общественного достояния.
Вы можете использовать их в качестве базы для своих собственных скриптов,
не беспокоясь об авторских правах.
