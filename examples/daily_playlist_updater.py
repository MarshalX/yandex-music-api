import datetime
import sys

from yandex_music import GeneratedPlaylist, Playlist
from yandex_music.client import Client

EXPECTED_ARGS_COUNT = 2

# Help text
if len(sys.argv) != EXPECTED_ARGS_COUNT:
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
    modified = datetime.datetime.strptime(DailyPlaylist.modified, '%Y-%m-%dT%H:%M:%S%z')
    if datetime.datetime.now(tz=modified.tzinfo).date() == modified.date():
        print('\x1b[6;30;43m' + 'Looks like it has been already updated today' + '\x1b[0m')
        sys.exit()

# Updated playlist
updated_playlist = client.users_playlists(user_id=DailyPlaylist.uid, kind=DailyPlaylist.kind)
assert isinstance(updated_playlist, Playlist)
assert updated_playlist.play_counter is not None

if updated_playlist.play_counter.updated and not DailyPlaylist.play_counter.updated:
    print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
else:
    print('\x1b[6;30;41m' + 'Something has gone wrong and nothing updated' + '\x1b[0m')

    # Debug information
    print(f'Before:\n    modified: {DailyPlaylist.modified}\n    PlayCounter: {DailyPlaylist.play_counter}')
    print(f'After:\n    modified: {updated_playlist.modified}\n    PlayCounter: {updated_playlist.play_counter}')
