import os

from yandex_music import Client


TOKEN = os.environ.get('TOKEN')

client = Client(TOKEN)

queues = client.queues_list()
# Последняя проигрываемая очередь всегда в начале списка
last_queue = client.queue(queues[0].id)

last_track_id = last_queue.get_current_track()
last_track = last_track_id.fetch_track()

artists = ', '.join(last_track.artists_name())
title = last_track.title
print(f'Сейчас играет: {artists} - {title}')

supplement = last_track.get_supplement()
if supplement.lyrics:
    print(supplement.lyrics.full_lyrics)
else:
    print('Текст песни отсутствует')
