# Получение альбома с треками

Пример получения информации об альбоме. Пример отображения треков вместе с исполнителями и названием.

```python
import os

from yandex_music import Client

# без авторизации недоступен список треков альбома
TOKEN = os.environ.get('TOKEN')
ALBUM_ID = 2832563

client = Client(TOKEN).init()

album = client.albums_with_tracks(ALBUM_ID)
tracks = []
for i, volume in enumerate(album.volumes):
    if len(album.volumes) > 1:
        tracks.append(f'💿 Диск {i + 1}')
    tracks += volume

text = 'АЛЬБОМ\n\n'
text += f'{album.title}\n'
text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
text += f'{album.year} · {album.genre}\n'

cover = album.cover_uri
if cover:
    text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

text += 'Список треков:'

print(text)

for track in tracks:
    if isinstance(track, str):
        print(track)
    else:
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)
        print(track.title + artists)
```
