# Обновление стрика дейлика

Отмечает "Плейлист дня" как прослушанный сегодня (добавляет +1 к счетчику).

```python
import sys
import datetime
from yandex_music.client import Client

# Help text
if len(sys.argv) == 1 or len(sys.argv) > 3:
    print('Usage: DailyPlaylistUpdater.py token')
    print('token - Authentication token')
    quit()
# Authorization
elif len(sys.argv) == 2:
    client = Client(sys.argv[1]).init()

# Current daily playlist
PersonalPlaylistBlocks = client.landing(blocks=['personalplaylists']).blocks[0]
DailyPlaylist = next(
    x.data.data for x in PersonalPlaylistBlocks.entities if x.data.data.generated_playlist_type == 'playlistOfTheDay'
)

# Check if we don't need to update it
if DailyPlaylist.play_counter.updated:
    modifiedDate = datetime.datetime.strptime(DailyPlaylist.modified, "%Y-%m-%dT%H:%M:%S%z").date()
    if datetime.datetime.now().date() == modifiedDate:
        print('\x1b[6;30;43m' + 'Looks like it has been already updated today' + '\x1b[0m')
        quit()

# Updated playlist
updatedPlaylist = client.users_playlists(user_id=DailyPlaylist.uid, kind=DailyPlaylist.kind)[0]

if updatedPlaylist.play_counter.updated and not DailyPlaylist.play_counter.updated:
    print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
else:
    print('\x1b[6;30;41m' + 'Something has gone wrong and nothing updated' + '\x1b[0m')

    # Debug information
    print('Before:\n    modified: %s\n    PlayCounter: %s' % (DailyPlaylist.modified, DailyPlaylist.play_counter))
    print('After:\n    modified: %s\n    PlayCounter: %s' % (updatedPlaylist.modified, updatedPlaylist.play_counter))
```
