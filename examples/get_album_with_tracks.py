import os
from typing import List, Union

from yandex_music import Client, Track

# без авторизации недоступен список треков альбома
TOKEN = os.environ.get('TOKEN')
ALBUM_ID = 2832563

client = Client(TOKEN).init()

album = client.albums_with_tracks(ALBUM_ID)
assert album is not None
assert album.volumes is not None
tracks: List[Union[str, Track]] = []
for i, volume in enumerate(album.volumes):
    if len(album.volumes) > 1:
        tracks.append(f'💿 Диск {i + 1}')
    tracks += volume

text = 'АЛЬБОМ\n\n'
text += f'{album.title}\n'
text += f'Исполнитель: {", ".join([str(artist.name) for artist in album.artists])}\n'
text += f'{album.year} · {album.genre}\n'

cover = album.cover_uri
if cover is not None and cover != '':
    text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

text += 'Список треков:'

print(text)

for track in tracks:
    if isinstance(track, str):
        print(track)
    else:
        artists = ''
        if len(track.artists) > 0:
            artists = ' - ' + ', '.join(str(artist.name) for artist in track.artists)
        print(str(track.title) + artists)
