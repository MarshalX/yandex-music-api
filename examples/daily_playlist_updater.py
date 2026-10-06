import datetime
import sys

from yandex_music import GeneratedPlaylist, Playlist
from yandex_music.client import Client

# Help text
if len(sys.argv) != 2:
    print('Usage: DailyPlaylistUpdater.py token')
    print('token - Authentication token')
    sys.exit()

# Authorization
client = Client(sys.argv[1]).init()

# Current daily playlist
landing = client.landing(blocks=['personalplaylists'])
assert landing is not None
PersonalPlaylistBlocks = landing.blocks[0]
DailyPlaylist = next(
    x.data.data
    for x in PersonalPlaylistBlocks.entities
    if isinstance(x.data, GeneratedPlaylist)
    and x.data.data is not None
    and x.data.data.generated_playlist_type == 'playlistOfTheDay'
)
assert DailyPlaylist.play_counter is not None
assert DailyPlaylist.modified is not None
assert DailyPlaylist.kind is not None

# Check if we don't need to update it
if DailyPlaylist.play_counter.updated:
    modifiedDate = datetime.datetime.strptime(DailyPlaylist.modified, '%Y-%m-%dT%H:%M:%S%z').date()
    if datetime.datetime.now().date() == modifiedDate:
        print('\x1b[6;30;43m' + 'Looks like it has been already updated today' + '\x1b[0m')
        sys.exit()

# Updated playlist
updatedPlaylist = client.users_playlists(user_id=DailyPlaylist.uid, kind=DailyPlaylist.kind)
assert isinstance(updatedPlaylist, Playlist)
assert updatedPlaylist.play_counter is not None

if updatedPlaylist.play_counter.updated and not DailyPlaylist.play_counter.updated:
    print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
else:
    print('\x1b[6;30;41m' + 'Something has gone wrong and nothing updated' + '\x1b[0m')

    # Debug information
    print('Before:\n    modified: %s\n    PlayCounter: %s' % (DailyPlaylist.modified, DailyPlaylist.play_counter))
    print('After:\n    modified: %s\n    PlayCounter: %s' % (updatedPlaylist.modified, updatedPlaylist.play_counter))
