import os

from yandex_music import Client

CHART_ID = 'world'
TOKEN = os.environ.get('TOKEN')

client = Client(TOKEN).init()
chart_info = client.chart(CHART_ID)
assert chart_info is not None
chart = chart_info.chart
assert chart is not None

text = [f'🏆 {chart.title}', chart.description if chart.description is not None else '', '', 'Треки:']

for track_short in chart.tracks:
    track, track_chart = track_short.track, track_short.chart
    assert track is not None
    assert track_chart is not None
    artists = ''
    if len(track.artists) > 0:
        artists = ' - ' + ', '.join(str(artist.name) for artist in track.artists)

    track_text = f'{track.title}{artists}'

    if track_chart.progress == 'down':
        track_text = '🔻 ' + track_text
    elif track_chart.progress == 'up':
        track_text = '🔺 ' + track_text
    elif track_chart.progress == 'new':
        track_text = '🆕 ' + track_text
    elif track_chart.position == 1:
        track_text = '👑 ' + track_text

    track_text = f'{track_chart.position} {track_text}'
    text.append(track_text)

print('\n'.join(text))
