import os

from yandex_music import Client


TOKEN = os.environ.get('TOKEN')

client = Client(TOKEN)

queues = client.queues_list()
# Последняя проигрываемая очередь всегда в начале списка
last_queue = client.queue(queues[0].id)

last_track_id = last_queue.tracks[last_queue.current_index]
last_track = client.tracks(f'{last_track_id.track_id}:{last_track_id.album_id}')[0]

artists = ', '.join([i.name for i in last_track.artists])
title = last_track.title
print(f'Сейчас играет: {artists} - {title}')

supplement = last_track.get_supplement()
if supplement.lyrics:
    print(supplement.lyrics.full_lyrics)
else:
    print('Текст песни отсутствует')
