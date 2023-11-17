#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from subprocess import call
from time import sleep
from typing import List

from yandex_music import Client

DEFAULT_CACHE_FOLDER = Path(__file__).resolve().parent / '.YMcache'
CONFIG_NAME = 'config'
MAX_ERRORS = 3

parser = argparse.ArgumentParser()
parser.add_argument('playlist', choices=('likes', 'user'), help='playlist type')
parser.add_argument('--playlist-name', help='name of user playlist')

parser.add_argument('--skip', metavar='N', type=int, help='skip first %(metavar)s tracks')
parser.add_argument('--shuffle', action='store_true', help='randomize tracks order')
parser.add_argument(
    '--token', default=DEFAULT_CACHE_FOLDER / CONFIG_NAME, help='YM API token as string or path to file'
)
parser.add_argument('--no-save-token', action='store_true', help="do'nt save token in cache folder")
parser.add_argument('--cache-folder', type=Path, default=DEFAULT_CACHE_FOLDER, help='cached tracks folder')
parser.add_argument('--audio-player', default='cvlc', help='player to use')
parser.add_argument(
    '--audio-player-args', action='append', default=[], help='args for --audio-player (can be specified multiple times)'
)
parser.add_argument('--print-args', action='store_true', help='print arguments (including default values) and exit')
args = parser.parse_args()

if args.audio_player is parser.get_default('audio_player') and args.audio_player_args is parser.get_default(
    'audio_player_args'
):
    args.audio_player_args = ['--play-and-exit', '--quiet']
player_cmd: List[int] = args.audio_player_args
player_cmd.insert(0, args.audio_player)
player_cmd.append('')  # will be replaced with filename

if args.print_args:
    print(args)
    sys.exit()

if isinstance(args.token, str) and re.match(r'^[A-Za-z0-9]{39}$', args.token):
    if not args.no_save_token:
        parser.get_default('token').write_text(args.token)
else:
    try:
        args.token = Path(args.token).read_text()
    except FileNotFoundError:
        print('Config file not found. Use --token to create it')
        sys.exit(2)

client = Client(args.token, report_unknown_fields=False).init()

print('Hello,', client.me.account.first_name)
if client.me.account.now and client.me.account.now.split('T')[0] == client.me.account.birthday:
    print('Happy birthday!')

if args.playlist == 'user':
    user_playlists = client.users_playlists_list()
    if not args.playlist_name:
        print('specify --playlist-name', [p.title for p in user_playlists])
        sys.exit(1)
    playlist = next((p for p in user_playlists if p.title == args.playlist_name), None)
    if playlist is None:
        print(f'playlist "{args.playlist_name}" not found')
        sys.exit(1)
    total_tracks = playlist.track_count
    print(f'Playing {playlist.title} ({playlist.playlist_id}). {total_tracks} track(s).')
    tracks = playlist.tracks if playlist.tracks else playlist.fetch_tracks()
elif args.playlist == 'likes':
    tracks = client.users_likes_tracks()
    total_tracks = len(tracks.tracks)
    print(f'Playing liked tracks. {total_tracks} track(s).')

if args.shuffle:
    from random import shuffle

    shuffle(tracks.tracks)

error_count = 0
for i, short_track in enumerate(tracks):
    if args.skip and args.skip > i:
        continue

    while error_count < MAX_ERRORS:
        try:
            track = short_track.track if short_track.track else short_track.fetchTrack()

            print(f'Now playing {i + 1}/{total_tracks}: ', end='')
            print('|'.join(a.name for a in track.artists), end='')
            print(f" [{'|'.join(a.title for a in track.albums)}]", '~', track.title)

            artist_dir = Path(f'{track.artists[0].name}_{track.artists[0].id}')
            album_dir = Path(f'{track.albums[0].title}_{track.albums[0].id}')
            file_path = args.cache_folder / artist_dir / album_dir / f'{track.title}_{track.id}.mp3'

            if not file_path.exists():
                print('Downloading...')
                file_path.parent.mkdir(parents=True, exist_ok=True)
                while error_count < MAX_ERRORS:
                    try:
                        track.download(file_path)
                        error_count = 0
                        break
                    except Exception as e:
                        print('Error:', e)
                        error_count += 1
                        sleep(1)

            player_cmd[-1] = file_path
            if call(player_cmd) == 0:
                error_count = 0
            else:
                error_count += 1
            break
        except Exception as e:
            print('Error:', e)
            error_count += 1
            sleep(1)
