from yandex_music.client import Client

# Аутентификация
# Если есть файл с токеном
import json
with open("credentials.json") as file:
    credentials = json.load(file)
token = credentials["token"]
client = Client(token)
# или
# client = Client.from_credentials('example@yandex.com', 'password')


def print_artist_title(track_short):
    # Для получения нужных значений обращаемся к свойству track обьекта класа TrackShort
    track = track_short.track
    print(track.artists[0]["name"],'-',track.title)
    # вывод должен быть в формате {Исполнитель} - {Название трека}
    # например: Apocalyptica - I Don't Care

liked_tracks = client.users_likes_tracks()

for track in liked_tracks[:10]:
    print_artist_title(track)
