import os

from yandex_music import Client

TOKEN = os.environ.get('TOKEN')
ALBUM_ID = 2832563

client = Client(TOKEN).init()

success = client.users_likes_albums_add(ALBUM_ID)
answer = 'Лайкнут' if success else 'Произошла ошибка'

print(answer)

success = client.users_likes_albums_remove(ALBUM_ID)
answer = 'Дизлайкнут' if success else 'Произошла ошибка'

print(answer)

# Тоже самое и в другими сущностями (плейлист, трек, исполнитель)
# client.users_likes_playlists_add(f'{user_id}:{playlist_id}')
# client.users_likes_playlists_remove(f'{user_id}:{playlist_id}')
# client.users_likes_tracks_add(track_id)
# client.users_likes_tracks_remove(track_id)
# и т.д. Читайте документацию.
