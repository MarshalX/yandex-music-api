# Получение чарта

Пример работы с чартом ЯМ. Получение треков, отображение позиций и их изменения с использованием эмодзи.

```python
import os

from yandex_music import Client


CHART_ID = 'world'
TOKEN = os.environ.get('TOKEN')

client = Client(TOKEN).init()
chart = client.chart(CHART_ID).chart

text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']

for track_short in chart.tracks:
    track, chart = track_short.track, track_short.chart
    artists = ''
    if track.artists:
        artists = ' - ' + ', '.join(artist.name for artist in track.artists)

    track_text = f'{track.title}{artists}'

    if chart.progress == 'down':
        track_text = '🔻 ' + track_text
    elif chart.progress == 'up':
        track_text = '🔺 ' + track_text
    elif chart.progress == 'new':
        track_text = '🆕 ' + track_text
    elif chart.position == 1:
        track_text = '👑 ' + track_text

    track_text = f'{chart.position} {track_text}'
    text.append(track_text)

print('\n'.join(text))
```
